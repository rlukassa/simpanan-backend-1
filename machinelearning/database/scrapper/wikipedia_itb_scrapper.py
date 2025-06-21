import requests
from bs4 import BeautifulSoup
import csv

# Ganti URL sesuai kebutuhan
url = "https://id.wikipedia.org/wiki/Institut_Teknologi_Bandung"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

rows = []
for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li"]):
    text = tag.get_text(strip=True)
    # Cari semua link di dalam tag
    links = [a['href'] for a in tag.find_all('a', href=True)]
    # Gabungkan semua link jadi satu string, pisahkan dengan spasi
    link_str = " ".join(links)
    # Simpan: tipe tag, isi teks, link (jika ada, di akhir baris)
    rows.append([tag.name, text, link_str])

with open("wikipedia_itb_full.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["type", "content", "links"])
    for row in rows:
        writer.writerow(row)

print("✅ Semua data dan link sudah disimpan di 'wikipedia_itb_full.csv'")
