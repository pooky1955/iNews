import React from "react"
import { Card } from "react-bootstrap"
import styled from "styled-components"

const StyledHeader = styled(Card.Header)`
  background : white;
`

const StyledTitle = styled(Card.Title)`
  text-align : center;
`

export const StyledCard = ({ title, header, body, links, fullPage }) => {
  return (
    <Card className = {fullPage? "full-page" : ""}>

      {header !== undefined &&
        <React.Fragment>
          <StyledHeader>{header}</StyledHeader>
          <hr className = "card-line"/>
        </React.Fragment>}
      <Card.Body as="span">
        <StyledTitle>{title}</StyledTitle>
        <Card.Text as="span">
          {body}
        </Card.Text>
        <br/>
        {links && links.map((link) => <a href={link} className = "card-link">{link}</a>)}
      </Card.Body>
    </Card>
  )
}

export default StyledCard