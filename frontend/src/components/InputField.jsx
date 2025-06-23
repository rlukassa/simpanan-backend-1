import React from 'react'

const InputField = ({ value, onChange, onKeyDown }) => {
  return (
    <input
      className="input-field"
      type="text"
      placeholder="Ketik pertanyaan tentang ITB..."
      value={value}
      onChange={onChange}
      onKeyDown={onKeyDown}
    />
  )
}

export default InputField