from fpdf import FPDF
import datetime
import os

class SecurityReport(FPDF):
    def header(self):
        # Üst Bilgi: Kurumsal ve Ciddi Görünüm
        self.set_fill_color(30, 30, 30) # Koyu Gri
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255) # Beyaz
        self.set_font('Arial', 'B', 16)
        self.cell(0, 15, 'MCP SENTINEL - OTONOM GUVENLIK SISTEMI', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'OTOMATIK OLAY ANALIZI VE ADLI BILISIM RAPORU', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Sayfa {self.page_no()} | MCP Sentinel v2.0 | Guvenli Hata Modu Aktif', 0, 0, 'C')

def clean_text(text):
    """FPDF Türkçe karakter hatasını önlemek için metni temizler."""
    chars = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o", "Ç": "C", "ç": "c"}
    for k, v in chars.items():
        text = text.replace(k, v)
    return text

def create_pdf_report(tool_name, arguments, reason, attack_chain="Bilgi Yok"):
    """XAI ve MITRE ATT&CK verilerini iceren gelismis adli rapor uretir."""
    try:
        pdf = SecurityReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Dosya ismine mikrosaniye ekleyerek çakışmayı önle
        unique_id = datetime.datetime.now().strftime('%H%M%S_%f')[:10]
        filename = f"RAPOR_{unique_id}.pdf"
        
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        full_path = os.path.join("reports", filename)

        # Metinleri temizle
        reason = clean_text(str(reason))
        tool_name = clean_text(str(tool_name))
        attack_chain = clean_text(str(attack_chain))

        # --- 1. OLAY OZETI ---
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"RAPOR TARIHI: {timestamp}", ln=True)
        pdf.ln(5)
        
        # --- 2. TEKNIK ANALIZ ---
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, "1. TEKNIK OLAY DETAYLARI", ln=True, fill=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, f"HEDEF ARAC: {tool_name}")
        pdf.multi_cell(0, 8, f"PARAMETRELER: {str(arguments)}")
        pdf.ln(5)
        
        # --- 3. DAVRANISSAL ANALIZ ---
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(255, 240, 240)
        pdf.cell(0, 10, "2. DAVRANISSAL SALDIRI ZINCIRI (CONTEXT)", ln=True, fill=True)
        pdf.set_font("Arial", size=10) # Courier bazen hata verir, Arial daha güvenli
        pdf.set_text_color(150, 0, 0)
        pdf.multi_cell(0, 7, f"Sistem Hafizasindaki Gecmis Kayitlar:\n{attack_chain}")
        pdf.ln(5)
        
        # --- 4. YAPAY ZEKA VE MITRE ---
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(230, 240, 255)
        pdf.cell(0, 10, "3. AI STRATEJIK ANALIZI VE MITRE ETIKETI", ln=True, fill=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, "KARAR: KRITIK TEHDIT TESPIT EDILDI VE ENGELLENDI", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, f"ADLI BILISIM GEREKCESI (XAI):\n{reason}")
        pdf.ln(10)

        # --- 5. SONUÇ ---
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 7, "Bu rapor, MCP Sentinel yapay zeka katmani tarafindan otonom uretilmistir.")

        pdf.output(full_path)
        print(f"[!] Rapor olusturuldu: {full_path}")
        return full_path
    except Exception as e:
        print(f"[!] PDF Hatasi: {e}")
        return None