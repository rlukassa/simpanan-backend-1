import React from 'react' // import react

const InputField = ({ value, onChange, onKeyDown }) => { // komponen input field
  return (
    <input
      className="input-field" // css class
      type="text" // tipe text
      placeholder="Ketik pertanyaan tentang ITB..." // placeholder text
      value={value} // value input
      onChange={onChange} // handler change
      onKeyDown={onKeyDown} // handler keydown
    />
  )
}

export default InputField // export komponen