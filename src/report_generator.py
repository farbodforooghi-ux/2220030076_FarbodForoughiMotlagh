from datetime import datetime
from html import escape
from pathlib import Path


def _table(headers, rows):
    head = "".join(f"<th>{escape(str(h))}</th>" for h in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def generate_html_report(target: str, ports: list[dict], banners: list[dict], prompt: str, ai_analysis: str, output_path: str = "reports/security_report.html") -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    port_rows = [[p.get("port"), p.get("protocol"), p.get("state"), p.get("service"), p.get("product"), p.get("version")] for p in ports]
    banner_rows = [[b.get("port"), b.get("service"), b.get("status"), b.get("banner")] for b in banners]
    html = f"""<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <title>AI Destekli Ağ Güvenlik Raporu</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #1f2937; background: #f8fafc; }}
    .container {{ max-width: 1100px; margin: auto; background: white; padding: 32px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,.08); }}
    h1, h2 {{ color: #111827; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0 28px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #e5e7eb; }}
    pre {{ white-space: pre-wrap; background: #0f172a; color: #e5e7eb; padding: 18px; border-radius: 8px; overflow-x: auto; }}
    .meta {{ background: #eff6ff; padding: 14px; border-left: 4px solid #2563eb; margin-bottom: 24px; }}
  </style>
</head>
<body>
<div class="container">
  <h1>AI Destekli Ağ Güvenlik Tarayıcı Raporu</h1>
  <div class="meta">
    <strong>Hedef IP:</strong> {escape(target)}<br>
    <strong>Rapor Tarihi:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}<br>
    <strong>Modüller:</strong> M1 Port Tarama + M6 Banner Grabbing
  </div>

  <h2>1. M1 Port Tarama Sonuçları</h2>
  {_table(['Port','Protokol','Durum','Servis','Ürün','Versiyon'], port_rows)}

  <h2>2. M6 Banner Grabbing Sonuçları</h2>
  {_table(['Port','Servis','Durum','Banner'], banner_rows)}

  <h2>3. AI API'ye Gönderilen Prompt</h2>
  <pre>{escape(prompt)}</pre>

  <h2>4. AI Güvenlik Analizi</h2>
  <pre>{escape(ai_analysis)}</pre>
</div>
</body>
</html>"""
    Path(output_path).write_text(html, encoding="utf-8")
    return output_path
