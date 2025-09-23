import requests
import csv
import time

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MyScraper/1.0)"
}

def fetch_json(url, headers=None, params=None, timeout=10):
    """Gửi request và trả về JSON"""
    h = headers or DEFAULT_HEADERS
    r = requests.get(url, headers=h, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def save_to_csv(filename, fieldnames, data):
    """data là list[dict]"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    url = "https://edge-api.pnj.io/ecom-frontend/v1/get-gold-price?zone=00"
    output_file = "pnj_gold.csv"
    delay = 1

    print(f"[+] Fetching API: {url}")
    data = fetch_json(url)

    # lấy dữ liệu vàng từ "data"
    items = data.get("data", [])
    chinhanh = data.get("chinhanh")
    updated = data.get("updateDate")

    results = []
    for item in items:
        row = {
            "Loại vàng": item.get("tensp"),
            "Mua": item.get("giamua"),
            "Bán": item.get("giaban"),
            "Cập nhật": updated,
            "Chi nhánh": chinhanh,
        }
        results.append(row)

    # lưu file CSV
    save_to_csv(output_file, ["Loại vàng", "Mua", "Bán", "Cập nhật", "Chi nhánh"], results)
    print(f"[✓] Saved {len(results)} records to {output_file}")

    time.sleep(delay)

if __name__ == "__main__":
    main()
