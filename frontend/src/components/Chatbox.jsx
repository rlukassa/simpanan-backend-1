import React from 'react'

const Chatbox = ({ messages }) => {
return (
    <div
        className="chatbox"
        style={{
            border: '1px solid #ccc',
            borderRadius: '8px',
            padding: '16px',
            height: '300px',
            overflowY: 'auto',
            background: '#fafafa',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: messages.length === 0 ? 'center' : 'flex-start',
            alignItems: 'center',
        }}
    >
        {messages.length === 0 ? (
            <div style={{ color: '#aaa', textAlign: 'center', display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%', height: '100%' }}>
                Belum ada pesan
            </div>
        ) : (
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', alignItems: 'flex-end', width: '100%' }}>
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        style={{
                            margin: '8px 0',
                            display: 'flex',
                            justifyContent: 'flex-end',
                            width: '100%',
                        }}
                    >
                        <span
                            style={{
                                background: msg.from === 'user' ? '#d1e7dd' : '#e2e3e5',
                                padding: '6px 12px',
                                borderRadius: '16px',
                                display: 'inline-block',
                                textAlign: 'justify',
                                maxWidth: '70%',
                                wordBreak: 'break-word',
                            }}
                        >
                            {msg.text}
                        </span>
                    </div>
                ))}
            </div>
        )}
    </div>
)
}

export default Chatbox