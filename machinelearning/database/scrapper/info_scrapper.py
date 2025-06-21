import requests
from bs4 import BeautifulSoup
import csv

# Ganti URL sesuai kebutuhan
url = "https://itb.ac.id"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

link_items = []
for a in soup.find_all("a", href=True):
    title = a.get_text(strip=True)
    href = a["href"]
    # Cari ringkasan di parent atau sibling
    summary = ""
    parent = a.parent
    next_tag = parent.find_next_sibling() if parent else None
    if next_tag and next_tag.name in ["p", "div"]:
        summary = next_tag.get_text(strip=True)
    elif parent and parent.name in ["p", "div"]:
        summary = parent.get_text(strip=True).replace(title, "")
    link_items.append((title, href, summary))

with open("info.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "url", "summary"])
    for title, href, summary in link_items:
        writer.writerow([title, href, summary])

print("✅ Semua link dan info terkait sudah disimpan di 'info.csv'")
