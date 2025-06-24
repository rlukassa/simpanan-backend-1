import { useState } from 'react' // hook state react
import './assets/App.css' // import css styles

import logoItb from './assets/Logo_Institut_Teknologi_Bandung.svg' // logo itb


import Chatbox from './components/Chatbox' // komponen chatbox
import InputField from './components/InputField' // komponen input field
import QueryButton from './components/QueryButton' // komponen query button
import { askToBackend } from './services/apicall' // api call service

function App() { // komponen utama app
  const [messages, setMessages] = useState([]) // state messages
  const [input, setInput] = useState("") // state input text
  const [isLoading, setIsLoading] = useState(false) // state loading
  const handleSend = async () => { // handler kirim pesan
    if (input.trim() === "" || isLoading) return // skip kalo kosong atau loading
    
    const userMessage = input.trim() // ambil user message
    setMessages(prev => [...prev, { from: 'user', text: userMessage }]) // tambah user message
    setInput("") // clear input
    setIsLoading(true) // set loading true
    
    try {
      const data = await askToBackend(userMessage) // panggil backend
      
      // Tambah jawaban utama
      setMessages(prev => [...prev, { from: 'bot', text: data.answer }]) // tambah bot response
      
      // Tambah bubble link jika ada
      if (data.hasLinks && data.links && data.links.length > 0) {
        const linkMessage = {
          from: 'bot',
          type: 'links',
          links: data.links,
          text: '🔗 Link terkait:'
        }
        setMessages(prev => [...prev, linkMessage]) // tambah bubble link
      }
      
    } catch (err) {
      setMessages(prev => [...prev, { // tambah error message
        from: 'bot', 
        text: 'Maaf, terjadi kesalahan saat menghubungi server. Silakan coba lagi.' // pesan error
      }])
    } finally {
      setIsLoading(false) // set loading false
    }
  }

  const handleKeyDown = (e) => { // handler keydown
    if (e.key === 'Enter' && !e.shiftKey) { // enter tanpa shift
      e.preventDefault() // prevent default
      handleSend() // kirim pesan
    }  }
  return (
    <div className="main-chat-container"> {/* container utama chat */}
      <div className="header-section"> {/* section header */}
        <img src={logoItb} alt="Logo ITB" className="itb-logo" /> {/* logo itb */}
        <h1>Chatbot ITB</h1> {/* judul chatbot */}
      </div>
      <div className="chatbox-section"> {/* section chatbox */}
        <Chatbox messages={messages} isLoading={isLoading} /> {/* komponen chatbox */}
      </div>      <div className="input-section"> {/* section input */}
        <InputField 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          onKeyDown={handleKeyDown}
        />
        <QueryButton 
          onClick={handleSend} 
          disabled={isLoading || input.trim() === ""}
        />
      </div>
      
      <div className="copyright-footer"> {/* footer copyright */}
        © 2025 rlukassa - All Rights Reserved {/* text copyright */}
      </div>
    </div>
  )
}

export default App
