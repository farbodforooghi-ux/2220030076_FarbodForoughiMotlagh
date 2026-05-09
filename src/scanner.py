import ipaddress
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class PortFinding:
    port: int
    protocol: str
    state: str
    service: str
    product: str
    version: str


def validate_private_target(target: str) -> str:
    """Allow only private lab IPs for the assignment."""
    try:
        ip = ipaddress.ip_address(target.strip())
    except ValueError as exc:
        raise ValueError("Target must be a valid IPv4 or IPv6 address.") from exc
    if not ip.is_private:
        raise ValueError("For ethical/legal reasons, this tool only scans private lab IP ranges, such as 192.168.x.x or 10.x.x.x.")
    return str(ip)


def run_nmap_scan(target: str) -> List[PortFinding]:
    """Run Nmap SYN scan + version detection and parse XML output."""
    target = validate_private_target(target)
    with tempfile.TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir) / "scan.xml"
        cmd = ["nmap", "-sS", "-sV", "-oX", str(xml_path), target]
        try:
            completed = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=180)
        except FileNotFoundError as exc:
            raise RuntimeError("Nmap is not installed. Install it with: sudo apt install nmap") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Nmap scan timed out. Check that your lab machine is reachable.") from exc

        if completed.returncode not in (0, 1):
            raise RuntimeError(f"Nmap failed:\n{completed.stderr}")
        if not xml_path.exists():
            raise RuntimeError("Nmap did not create XML output.")
        return parse_nmap_xml(xml_path)


def parse_nmap_xml(xml_path: Path) -> List[PortFinding]:
    findings: List[PortFinding] = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for port_node in root.findall(".//port"):
        state_node = port_node.find("state")
        if state_node is None or state_node.get("state") != "open":
            continue
        service_node = port_node.find("service")
        findings.append(
            PortFinding(
                port=int(port_node.get("portid", "0")),
                protocol=port_node.get("protocol", "tcp"),
                state=state_node.get("state", "unknown"),
                service=(service_node.get("name", "unknown") if service_node is not None else "unknown"),
                product=(service_node.get("product", "") if service_node is not None else ""),
                version=(service_node.get("version", "") if service_node is not None else ""),
            )
        )
    return findings


def findings_to_dicts(findings: List[PortFinding]) -> list[dict]:
    return [asdict(item) for item in findings]
