import React from "react"
import {Button} from "react-bootstrap"
import {goToPage} from "../App"
export const NotSearchedNews = () => {
  return (
    <div style = {{position : "absolute",top : "50%",left : "50%",transform : "translate(-50%,-50%)"}}>
      <h2>It seems like you haven't searched for news yet...</h2>
      <Button variant="outline-secondary" onClick = {()=>goToPage(0)}>Search for news</Button>
    </div>

  )
}

export default NotSearchedNews