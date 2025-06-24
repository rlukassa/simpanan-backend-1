import React from 'react' // import react

const QueryButton = ({ onClick, disabled = false }) => { // komponen query button
  return (
    <button
      className="query-button" // css class
      onClick={onClick} // handler click
      disabled={disabled} // disabled state
    >
      <span>Kirim</span> {/* text button */}
      <span style={{ marginLeft: '0.5rem' }}>→</span> {/* arrow icon */}
    </button>
  )
}

export default QueryButton // export komponen