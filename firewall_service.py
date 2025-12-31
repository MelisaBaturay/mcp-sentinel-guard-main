import os

BLACKLIST_FILE = "blacklist.txt"

def get_blacklisted_ips():
    """Yasaklı kullanıcı/IP listesini döner."""
    if not os.path.exists(BLACKLIST_FILE):
        return []
    try:
        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except:
        return []

def add_to_blacklist(ip_or_user):
    """Kullanıcıyı kara listeye ekler."""
    blacklisted = get_blacklisted_ips()
    if ip_or_user not in blacklisted:
        with open(BLACKLIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{ip_or_user}\n")
        print(f"🚫 {ip_or_user} KARA LİSTEYE ALINDI!")

def check_security_violation(logs, target_user):
    """
    Davranışsal Analiz: Son 10 logu kontrol et, 
    eğer aynı kullanıcı 3 kez engellendiyse banla.
    """
    if not logs:
        return False
        
    danger_count = 0
    # Loglar liste değilse (dosya okumaysa) listeye çevir
    for log in logs[-10:]:
        # Log içeriğini string olarak kontrol et
        log_str = str(log)
        if target_user in log_str and "ENGELLENDI" in log_str:
            danger_count += 1
    
    if danger_count >= 3:
        add_to_blacklist(target_user)
        return True
    return False