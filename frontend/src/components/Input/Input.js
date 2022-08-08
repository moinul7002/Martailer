import React from 'react'
import './Input.css'

const Input = (props) => {
  const { bgColor, border, fontSize, placeholder, brRadius, height, name, value, label, onChange } = props
  const styleSheet = {
    backgroundColor: bgColor || 'white',
    border: border || '1px solid gray',
    fontSize: fontSize || '',
    borderRadius: brRadius || '',
    height: height || '30px'
  }
  return (
    <>   
    {label && <div style={{marginBottom:'10px'}}>{label}</div>} 
    <div style={styleSheet} className='input-wrapper'>
      <input onChange={(e)=>onChange(e)} name={name} value={value} placeholder={placeholder || ''} />
    </div>
    </>

  )
}
export default Input
