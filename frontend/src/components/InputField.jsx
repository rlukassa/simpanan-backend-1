import React from 'react'

// pake arrow function 
const InputField = ({ value, onChange, onKeyDown }) => {
  return (
    <input
      className="input-field"
      type="text"
      placeholder="Ketik pesan..."
      value={value} // pengganti placeholder, ketika diketik maka akan menghapus placeholder dan mengetik 
      onChange={onChange} // 
      onKeyDown={onKeyDown}
      style={{flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #ccc', marginRight: '8px'}}
    />
  )
}

export default InputField