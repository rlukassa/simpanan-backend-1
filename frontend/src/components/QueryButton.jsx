import React from 'react'

const QueryButton = ({ onClick, disabled = false }) => {
  return (
    <button
      className="query-button"
      onClick={onClick}
      disabled={disabled}
    >
      <span>Kirim</span>
      <span style={{ marginLeft: '0.5rem' }}>→</span>
    </button>
  )
}

export default QueryButton