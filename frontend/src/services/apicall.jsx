// API call ke backend (axios, fetch)

// Fungsi untuk memanggil backend (POST ke /ask)

// mengirim pertanyaan ke backend lewat endpoint /ask pakai fetch post
export async function askToBackend(question) {
  const response = await fetch('http://localhost:5000/ask', { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  if (!response.ok) throw new Error('Gagal menghubungi server')
  return response.json()
}