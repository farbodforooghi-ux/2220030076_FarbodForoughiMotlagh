import socket
from dataclasses import dataclass, asdict
from typing import List

from scanner import PortFinding


@dataclass
class BannerFinding:
    port: int
    service: str
    banner: str
    status: str


def grab_banner(host: str, port: int, timeout: float = 2.0) -> BannerFinding:
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            try:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            except OSError:
                pass
            try:
                data = sock.recv(512)
                banner = data.decode(errors="replace").strip()
            except socket.timeout:
                banner = "No banner received before timeout."
            return BannerFinding(port=port, service="unknown", banner=banner[:500], status="success")
    except Exception as exc:
        return BannerFinding(port=port, service="unknown", banner=str(exc), status="failed")


def run_banner_grabbing(host: str, ports: List[PortFinding]) -> List[BannerFinding]:
    results: List[BannerFinding] = []
    for finding in ports:
        banner = grab_banner(host, finding.port)
        banner.service = finding.service
        results.append(banner)
    return results


def banners_to_dicts(banners: List[BannerFinding]) -> list[dict]:
    return [asdict(item) for item in banners]
