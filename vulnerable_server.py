# BU DOSYA: GERÇEK İŞLEMİ YAPAN SAVUNMASIZ SUNUCUDUR (SERVER LAYER)
# İçinde hiçbir güvenlik kontrolü yoktur.

def unsafe_delete_files(path: str) -> str:
    """Gerçek silme işlemini yapan fonksiyon."""
    # Gerçek hayatta burada os.remove(path) olurdu.
    return f"DOSYA SİLİNDİ: {path} (Vulnerable Server tarafından yapıldı)"

def unsafe_read_data(query: str) -> str:
    """Gerçek okuma işlemini yapan fonksiyon."""
    # Gerçek hayatta burada veritabanı sorgusu olurdu.
    return f"VERİ OKUNDU: {query} (Vulnerable Server'dan geldi)"

# --- YENİ EKLENEN TEHLİKELİ FONKSİYONLAR ---

def unsafe_steal_credentials(target_user: str) -> str:
    """Simülasyon: Kullanıcı şifrelerini veritabanından çeker."""
    # Gerçek hayatta burası veritabanına giderdi.
    return f"GIZLI VERI SIZDIRILDI! {target_user} icin sifreler: 123456, admin_pass, secret_key"

def unsafe_shutdown_server(force: bool) -> str:
    """Simülasyon: Sunucuyu uzaktan kapatır."""
    return "SİSTEM KAPATILIYOR... TÜM SERVİSLER DURDURULDU."