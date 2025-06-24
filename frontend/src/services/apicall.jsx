// API Communication Layer - komunikasi dengan backend
// Kirim pertanyaan user ke backend dan terima response JSON

export async function askToBackend(question) {  // Fungsi kirim pertanyaan ke backend
  const response = await fetch('http://localhost:5000/ask', {  // POST request ke endpoint /ask
    method: 'POST',  // Method HTTP POST
    headers: { 'Content-Type': 'application/json' },  // Header JSON
    body: JSON.stringify({ question })  // Body request dengan question
  })
  if (!response.ok) throw new Error('Gagal koneksi server')  // Cek response OK
  return response.json()  // Return JSON response
}