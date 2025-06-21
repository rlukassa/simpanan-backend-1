import React from 'react'

const QueryButton = ({ onClick }) => {
  return (
    <button
      className="query-button"
      onClick={onClick}
      style={{padding: '10px 20px', borderRadius: '8px', background: '#2563eb', color: 'white', border: 'none', cursor: 'pointer'}}
    >
      Kirim
    </button>
  )
}

export default QueryButton