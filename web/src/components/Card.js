import React from "react"
import { Card } from "react-bootstrap"
import styled from "styled-components"

const StyledHeader = styled(Card.Header)`
  background : white;
`

const StyledTitle = styled(Card.Title)`
  text-align : center;
`

export const StyledCard = ({ title, header, body, links }) => {
  return (
    <Card>

      {header !== undefined &&
        <React.Fragment>
          <StyledHeader>{header}</StyledHeader>
          <hr className = "card-line"/>
        </React.Fragment>}
      <Card.Body>
        <StyledTitle>{title}</StyledTitle>
        <Card.Text>
          {body}
        </Card.Text>
        {links && links.map((link) => <Card.Link className = "card-link"><a href={link}>{link}</a></Card.Link>)}
      </Card.Body>
    </Card>
  )
}

export default StyledCard