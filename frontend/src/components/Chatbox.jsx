import React from 'react'
import logoItb from '../assets/Logo_Institut_Teknologi_Bandung.svg'

const TypingIndicator = () => (
    <div className="message-bubble bot" style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
    }}>
        <div className="sender-name" style={{
            fontSize: '0.75rem',
            color: '#64748b',
            marginBottom: '0.25rem',
            paddingLeft: '0.5rem',
            fontWeight: '500'
        }}>
            Roga
        </div>
        <div className="message-text bot" style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem',
            padding: '1rem 1.25rem'
        }}>
            <span>sedang mengetik</span>
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
                <div className="chatbot-icon">
                    <img 
                        src={logoItb} 
                        alt="Logo ITB" 
                        className="chatbot-logo"
                        onError={(e) => {
                            console.log('Chatbot logo failed to load, using fallback');
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'inline-block';
                        }}
                    />
                    <span className="chatbot-logo-fallback" style={{display: 'none', fontSize: '64px'}}>🎓</span>
                </div>
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
                            flexDirection: 'column',
                            alignItems: msg.from === 'user' ? 'flex-end' : 'flex-start',
                        }}
                    >
                        <div className="sender-name" style={{
                            fontSize: '0.75rem',
                            color: '#64748b',
                            marginBottom: '0.25rem',
                            paddingLeft: msg.from === 'user' ? '0' : '0.5rem',
                            paddingRight: msg.from === 'user' ? '0.5rem' : '0',
                            fontWeight: '500'
                        }}>
                            {msg.from === 'user' ? 'User' : 'Roga'}
                        </div>
                        <div className={`message-text ${msg.from}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && <TypingIndicator />}
            </div>
        )}
        
        <style jsx>{`
            .chatbot-logo {
                width: 64px;
                height: 64px;
                object-fit: contain;
                filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.15));
                transition: all 0.3s ease;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.1);
                padding: 8px;
            }
            
            .chatbot-logo:hover {
                transform: scale(1.05);
                filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.2));
            }
            
            .chatbot-logo-fallback {
                line-height: 1;
                filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
                animation: bounce 2s ease-in-out infinite;
            }
            
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% {
                    transform: translateY(0);
                }
                40% {
                    transform: translateY(-10px);
                }
                60% {
                    transform: translateY(-5px);
                }
            }
            
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
            
            @media (max-width: 640px) {
                .chatbot-logo {
                    width: 56px;
                    height: 56px;
                }
                .chatbot-logo-fallback {
                    font-size: 56px !important;
                }
            }
            
            @media (max-width: 480px) {
                .chatbot-logo {
                    width: 48px;
                    height: 48px;
                }
                .chatbot-logo-fallback {
                    font-size: 48px !important;
                }
            }
        `}</style>
    </div>
)
}

export default Chatbox