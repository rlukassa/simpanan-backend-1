import requests
from bs4 import BeautifulSoup
import csv

url = "https://itb.ac.id/tentang-itb"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

rows = []
for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li"]):
    text = tag.get_text(strip=True)
    links = [a['href'] for a in tag.find_all('a', href=True)]
    link_str = " ".join(links)
    rows.append([tag.name, text, link_str])

with open("tentang_itb_full.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["type", "content", "links"])
    for row in rows:
        writer.writerow(row)

print("✅ Semua data dan link sudah disimpan di 'tentang_itb_full.csv'")
