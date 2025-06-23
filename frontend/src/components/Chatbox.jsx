import React from 'react'

const TypingIndicator = () => (
    <div className="message-bubble bot">
        <div className="message-text bot" style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem',
            padding: '1rem 1.25rem'
        }}>
            <span>ITB Bot sedang mengetik</span>
            <div style={{ display: 'flex', gap: '2px' }}>
                <div style={{
                    width: '6px',
                    height: '6px',
                    borderRadius: '50%',
                    backgroundColor: '#667eea',
                    animation: 'typingDot 1.4s infinite ease-in-out'
                }}></div>
                <div style={{
                    width: '6px',
                    height: '6px',
                    borderRadius: '50%',
                    backgroundColor: '#667eea',
                    animation: 'typingDot 1.4s infinite ease-in-out 0.2s'
                }}></div>
                <div style={{
                    width: '6px',
                    height: '6px',
                    borderRadius: '50%',
                    backgroundColor: '#667eea',
                    animation: 'typingDot 1.4s infinite ease-in-out 0.4s'
                }}></div>
            </div>
        </div>
    </div>
)

const Chatbox = ({ messages, isLoading = false }) => {
return (
    <div className="chatbox">
        {messages.length === 0 && !isLoading ? (
            <div className="empty-state">
                <div className="chatbot-icon">🎓</div>
                <div>
                    <div style={{ fontWeight: '600', marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                        Selamat datang di Chatbot ITB!
                    </div>
                    <div style={{ fontSize: '0.9rem', lineHeight: '1.4' }}>
                        Tanyakan apapun tentang Institut Teknologi Bandung
                        <br />
                        <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>
                            Contoh: "Apa itu ITB?", "Fakultas di ITB", "Sejarah ITB"
                        </span>
                    </div>
                </div>
            </div>
        ) : (
            <div style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                gap: '0.5rem',
                height: '100%',
                paddingBottom: '1rem'
            }}>
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`message-bubble ${msg.from}`}
                        style={{
                            display: 'flex',
                            justifyContent: msg.from === 'user' ? 'flex-end' : 'flex-start',
                        }}
                    >
                        <div className={`message-text ${msg.from}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && <TypingIndicator />}
            </div>
        )}
        
        <style jsx>{`
            @keyframes typingDot {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
        `}</style>
    </div>
)
}

export default Chatbox