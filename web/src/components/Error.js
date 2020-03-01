import React from "react"

export const Error = ({ actionString }) => {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", background: "white" }}>
      <div className="p-2">
        An error occured while {actionString}. That's all we know.
    </div>
    </div>
  )
}

export default Error