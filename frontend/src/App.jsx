// Entry point React 


import { useState } from 'react'
import './assets/App.css'

import Chatbox from './components/Chatbox' // Importing components
import InputField from './components/InputField'
import QueryButton from './components/QueryButton'
import { askToBackend } from './services/apicall'

function App() {
  const [messages, setMessages] = useState([]) // menambah state untuk meenyimpan pesan 
  const [input, setInput] = useState("")

  // Handler untuk mengirim pesan
  // jadi pas enter, handleSend bakal dipanggil, dan pesannya di masukin ke {sini}
  const handleSend = async () => {
    if (input.trim() === "") return // kalo kosong, gak kirim 
    setMessages([...messages, { from: 'user', text: input }]) // {sini}
    try { // message nya bakal dikirim ke backkend 
      const data = await askToBackend(input) // 
      setMessages(msgs => [...msgs, { from: 'bot', text: data.answer }])
    } catch (err) { // kalo ada error, misalnya server gak jalan, maka tampilkan pesan error
      setMessages(msgs => [...msgs, { from: 'bot', text: 'Gagal menghubungi server.' }])
    }
    setInput("") // kosongkan input 
  }

  // Handler untuk enter
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend() // kalo enter ditekan, maka kirim pesan dengan hhandleSend
  }

  return (
    <div className="main-chat-container">
      <h1>Chatbot Informasi Khusus ITB</h1>
      <div className="chatbox-section">
        <Chatbox messages={messages} />
      </div>
      <div className="input-section" style={{display: 'flex', marginTop: '16px'}}>
        <InputField value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown} />
        {/* jadi 3 parameter dari inputfield ini bakal ganti value input, dan juga onKeyDownny buat jalanin handleKeyDown (enter) */}
        <QueryButton onClick={handleSend} />
      </div>
    </div>
  )
}

export default App
