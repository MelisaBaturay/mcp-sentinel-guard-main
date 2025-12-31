import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# --- AYARLAR ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MY_EMAIL = os.getenv("GMAIL_USER")       
MY_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")       
TO_EMAIL = os.getenv("GMAIL_USER")       

def send_alert_email(tool_name, user_id, reason, severity="ORANGE"):
    """
    Saldırının kritiklik seviyesine (Severity) göre özelleştirilmiş 
    akademik standartlarda bir siber güvenlik bildirimi gönderir.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # --- Akademik Triage (Önceliklendirme) Konfigürasyonu ---
    config = {
        "GREEN":  {"label": "DUSUK", "color": "#4caf50", "subject": "[INFO] MCP Sentinel: Hafif Supheli Hareket"},
        "ORANGE": {"label": "ORTA", "color": "#ff9800", "subject": "[UYARI] MCP Sentinel: Olasi Saldiri Engellendi"},
        "RED":    {"label": "KRITIK", "color": "#d32f2f", "subject": "[ACIL] MCP Sentinel: KRITIK SALDIRI ZINCIRI!"}
    }
    
    current_cfg = config.get(severity, config["ORANGE"])
    subject = current_cfg["subject"]
    header_color = current_cfg["color"]

    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="background-color: {header_color}; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">SİBER GÜVENLİK OLAY BİLDİRİMİ</h1>
            <p style="margin: 5px 0 0 0;"><strong>Kritiklik Seviyesi: {current_cfg['label']}</strong></p>
        </div>
        <div style="padding: 25px; border: 1px solid #ddd; background-color: #fafafa;">
            <p><strong>Sayın Yönetici,</strong></p>
            <p>Otonom Savunma Sistemi (Sentinel Gateway), MCP araçlarına yönelik bir tehdit zinciri tespit ederek müdahale etmiştir.</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr style="background-color: #eee;">
                    <td style="padding: 10px; border: 1px solid #ccc;"><strong>Zaman</strong></td>
                    <td style="padding: 10px; border: 1px solid #ccc;">{timestamp}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ccc;"><strong>Tespit Edilen Varlık</strong></td>
                    <td style="padding: 10px; border: 1px solid #ccc;">{user_id}</td>
                </tr>
                <tr style="background-color: #eee;">
                    <td style="padding: 10px; border: 1px solid #ccc;"><strong>Hedef MCP Aracı</strong></td>
                    <td style="padding: 10px; border: 1px solid #ccc;">{tool_name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ccc;"><strong>Analiz Gerekçesi</strong></td>
                    <td style="padding: 10px; border: 1px solid #ccc; color: {header_color};"><strong>{reason}</strong></td>
                </tr>
            </table>
            <p style="margin-top: 20px; font-size: 12px; color: #666;">
                *Bu rapor, bağlamsal saldırı hafızası kullanılarak üretilmiştir. 
                Saldırgan otonom olarak kara listeye alınmış olabilir. Lütfen Dashboard'u kontrol ediniz.
            </p>
        </div>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = MY_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        
        print(f"[MAIL] {severity} seviyeli bildirim basariyla gonderildi.")
        return True
    except Exception as e:
        print(f"[MAIL HATA] {e}")
        return False