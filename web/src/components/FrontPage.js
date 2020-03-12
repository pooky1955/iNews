import React, { useState } from "react"
import { Page } from "./Page";
import { Redirect } from "react-router-dom";
import iconPng from "./images/icon.png"
import styled from "styled-components"
import { Error } from "./Error"
import { Loader } from "./Loader"
import { Button, Form } from "react-bootstrap"
import { urlExtract } from "../util";


const StyledIcon = styled.img`
  width : 30vmin;
`

function getField(e, name) {
  let formElement = e.currentTarget
  let data = new FormData(formElement)
  let fieldValue = data.get(name)
  return fieldValue
}

export const FrontPage = () => {
  const [shouldRedirect, setShouldRedirect] = useState(false)
  const [data, setData] = useState({})

  if (shouldRedirect) {
    const {encodedUrl} = data
    return <Redirect to={`/dashboard/${encodedUrl}`} />

  } else {
    return (
      <Page background="white">

        <div className = "app-frontpage-container">
          <div className = "app-title">iNews</div>
          <div className = "app-description">iNews is a fake news detector based on machine learning and NLP</div>
          <StyledIcon src={iconPng} className = "app-mascot"></StyledIcon>

          <Form onSubmit={async (e) => {
            e.preventDefault()
            let url = getField(e,"url")
            let encodedUrl = encodeURIComponent(url)
            setData({encodedUrl})
            setShouldRedirect(true)
          }}>
            <div className = "app-prompt mb-3">Let's test your claim!</div>
            <Form.Control className = "app-input" name="url" type="text" placeholder="Link"></Form.Control>
            <Button  style = {{display :"block", width : "100%"}}  variant = "outline-success" type = "submit" className = "mt-3 app-submit-button">Verify</Button>
          </Form>
        </div>
      </Page>
    )
  }
}
export default FrontPage