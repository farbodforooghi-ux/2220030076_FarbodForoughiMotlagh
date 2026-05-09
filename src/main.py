import json
from pathlib import Path

from ai_analysis import analyze_with_gemini, build_prompt
from banner_grabber import banners_to_dicts, run_banner_grabbing
from report_generator import generate_html_report
from scanner import findings_to_dicts, run_nmap_scan, validate_private_target


def main():
    print("AI Destekli Ağ Güvenlik Tarayıcı")
    print("Etik uyarı: Yalnızca kendi lab makinenizi tarayın. Örn: Metasploitable, DVWA.")
    target = input("Hedef IP adresini girin (192.168.x.x veya 10.x.x.x): ").strip()
    target = validate_private_target(target)

    print("\n[1/4] Nmap port taraması başlıyor...")
    port_findings = run_nmap_scan(target)
    ports = findings_to_dicts(port_findings)
    print(json.dumps(ports, indent=2, ensure_ascii=False))

    print("\n[2/4] M6 Banner Grabbing çalışıyor...")
    banner_findings = run_banner_grabbing(target, port_findings)
    banners = banners_to_dicts(banner_findings)
    print(json.dumps(banners, indent=2, ensure_ascii=False))

    print("\n[3/4] AI analizi oluşturuluyor...")
    prompt = build_prompt(target, ports, banners)
    ai_text = analyze_with_gemini(prompt)
    print(ai_text)

    print("\n[4/4] HTML rapor oluşturuluyor...")
    report_path = generate_html_report(target, ports, banners, prompt, ai_text)
    print(f"Rapor hazır: {Path(report_path).resolve()}")


if __name__ == "__main__":
    main()
