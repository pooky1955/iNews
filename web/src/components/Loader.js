import React from "react"
import { Spinner } from "react-bootstrap"
export const Loader = ({ text ,backgroundColor="white"}) => {
  return (
     <div style = {{display : "flex",height : '100%',alignItems : "center",justifyContent: "center",background : backgroundColor}}> 
      <div style={{ textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center"}}>
        <Spinner animation="border" className="mb-4 mt-4"></Spinner>
        <p>{text}</p>
      </div>
      </div>
  )
}

export default Loader