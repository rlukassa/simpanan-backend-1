# Enhanced Data Loader - Load processed high-quality CSV
import pandas as pd  # Library untuk manipulasi data
import os  # OS interface untuk file operations
import sys  # System utilities

currentDir = os.path.dirname(os.path.abspath(__file__))  # Dapatkan direktori saat ini
sys.path.append(currentDir)  # Tambah ke Python path

def loadCsvData():  # Load enhanced dataset dari processed CSV
    processedFile = os.path.join(  # Path ke file processed
        os.path.dirname(__file__), 
        'database', 
        'processed', 
        'itb_chatbot_high_quality_20250621_190153.csv'
    )

    if os.path.exists(processedFile):  # Cek file processed ada
        try:  # Coba load file processed
            print(f"📂 Loading enhanced dataset: {os.path.basename(processedFile)}")  # Log loading
            df = pd.read_csv(processedFile)  # Baca CSV dengan pandas

            allData = []  # List untuk semua data
            for _, row in df.iterrows():  # Loop setiap row
                entry = {  # Format data entry
                    'source': row['data_source'],  # Sumber data
                    'content': row['content'],  # Konten asli
                    'processed_content': row['content_cleaned'],  # Konten bersih
                    'category': row['category'],  # Kategori konten
                    'quality_score': row['quality_score'],  # Skor kualitas
                    'content_length': row['content_length'],  # Panjang konten
                    'type': row.get('type', ''),  # Tipe konten
                    'links': row.get('links', ''),  # Link terkait
                    'record_id': row['record_id']  # ID record
                }
                allData.append(entry)  # Tambah ke list

            print(f"✅ Loaded {len(allData)} high-quality entries")  # Log sukses
            print(f"📊 Categories: {len(set(entry['category'] for entry in allData))}")  # Log kategori
            print(f"⭐ Avg quality: {sum(entry['quality_score'] for entry in allData)/len(allData):.1f}/100")  # Log rata-rata kualitas

            return allData  # Return data

        except Exception as e:  # Tangkap error loading
            print(f"⚠️  Error loading processed data: {e}")  # Log error
            print("🔄 Falling back to original CSV files...")  # Log fallback
    else:  # File processed tidak ada
        print(f"⚠️  Processed file not found: {processedFile}")  # Log not found
        print("🔄 Using original CSV files...")  # Log fallback

    return loadOriginalCsvData()  # Fallback ke original

def loadOriginalCsvData():  # Load original CSV files
    dataDir = os.path.join(os.path.dirname(__file__), 'database', 'data')  # Path ke data directory

    csvFiles = [  # List file CSV asli
        'tentangITB.csv',  # File tentang ITB
        'wikipediaITB.csv',  # File Wikipedia ITB
        'multikampusITB.csv'  # File multikampus ITB
    ]

    allData = []  # List untuk semua data

    for csvFile in csvFiles:  # Loop setiap file CSV
        filePath = os.path.join(dataDir, csvFile)  # Path lengkap file
        if os.path.exists(filePath) and os.path.getsize(filePath) > 0:  # Cek file ada dan tidak kosong
            try:  # Coba load file
                df = pd.read_csv(filePath)  # Baca CSV
                if not df.empty and 'content' in df.columns:  # Cek data valid
                    dfFiltered = df[df['content'].notna() & (df['content'] != '')]  # Filter data kosong

                    for _, row in dfFiltered.iterrows():  # Loop setiap row
                        content = str(row['content']).strip()  # Ambil konten bersih
                        if content and len(content) >= 5:  # Cek konten valid
                            entry = {  # Format data entry
                                'source': csvFile.replace('.csv', ''),  # Source tanpa extension
                                'content': content,  # Konten asli
                                'processed_content': content.lower(),  # Konten lowercase
                                'type': row.get('type', ''),  # Tipe konten
                                'links': row.get('links', ''),  # Link terkait
                                'category': 'uncategorized',  # Kategori default
                                'quality_score': 50,  # Skor default
                                'content_length': len(content)  # Panjang konten
                            }
                            allData.append(entry)  # Tambah ke list

            except Exception as e:  # Tangkap error loading
                print(f"Error loading {csvFile}: {e}")  # Log error
                continue  # Lanjut ke file berikutnya

    print(f"Loaded {len(allData)} data entries from original CSV files")  # Log total loaded
    return allData  # Return data

def getSampleData():  # Ambil sample data untuk testing
    data = loadCsvData()  # Load semua data
    return data[:10] if data else []  # Return 10 data pertama atau empty

if __name__ == "__main__":  # Test script
    data = loadCsvData()  # Test load data
    print(f"\nTotal entries: {len(data)}")  # Print total
    
    if data:  # Jika ada data
        print("\nSample entries:")  # Print header
        for i, entry in enumerate(data[:3]):  # Loop 3 entry pertama
            score = entry.get('quality_score', 'N/A')  # Ambil score
            category = entry.get('category', 'uncategorized')  # Ambil kategori
            print(f"{i+1}. [{entry['source']}] {category} ({score}) {entry['content'][:80]}...")  # Print sample
