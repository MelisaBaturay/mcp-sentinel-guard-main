import json
import uuid
import random
import datetime
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- KONFİGÜRASYON ---
url = "http://localhost:8086"
token = "FR9fpgDtATsW2rJA6RhsFR24azA2WFUEVbgiQ6btPbKpjWQ8Rqtiv1K14hFiYqR5Wq0e-JQPdFXMbFtTkH_0ig==" 
org = "sentinel_org"
bucket = "sentinel_logs"

# --- SENİN ŞABLONUNA UYGUN SENARYOLAR ---
# Bu kısımdaki 'error_message' siber saldırı adını, 'status_code' engelleme durumunu tutar.
scenarios = [
    {"message": "DROP TABLE users; --", "status_code": 403, "error_message": "SQL Injection"},
    {"message": "<script>alert('XSS')</script>", "status_code": 403, "error_message": "XSS Attack"},
    {"message": "Bir dosya sileceğim, yardım et", "status_code": 403, "error_message": "Unauthorized Access"},
    {"message": "Sisteme giriş yapmak istiyorum", "status_code": 200, "error_message": None},
    {"message": "SELECT * FROM products", "status_code": 200, "error_message": None}
]

def generate_and_sync_data():
    selected = random.choice(scenarios)
    
    # --- SENİN ŞABLONUNLA BİREBİR AYNI İSİMLER ---
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "request_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1000, 9999)}",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "ip_address": f"{random.randint(70,95)}.{random.randint(100,200)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "model": "gemini-2.0-flash",
        "message": selected["message"],
        "tokens_used": random.randint(10, 80),
        "response_time_ms": random.randint(400, 1800),
        "status_code": selected["status_code"],
        "error_message": selected["error_message"]
    }

    # 1. security_dataset.json Dosyasına Yazma
    file_path = "security_dataset.json"
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []
    data.append(log_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # 2. InfluxDB'ye Gönderme (Grafana için isimleri eşliyoruz)
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    point = Point("security_events") \
        .tag("ip_address", log_entry["ip_address"]) \
        .tag("error_message", str(log_entry["error_message"])) \
        .tag("status_code", str(log_entry["status_code"])) \
        .field("tokens_used", log_entry["tokens_used"]) \
        .field("response_time_ms", log_entry["response_time_ms"]) \
        .field("event_count", 1) \
        .time(datetime.datetime.utcnow(), WritePrecision.NS)
    
    write_api.write(bucket, org, point)
    client.close()
    
    print(f"BAŞARILI: {log_entry['error_message'] if log_entry['error_message'] else 'Güvenli İşlem'} kaydedildi.")

if __name__ == "__main__":
    generate_and_sync_data()