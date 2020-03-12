import React from "react"
import { Card } from "react-bootstrap"
import styled from "styled-components"


const StyledTitle = styled(Card.Title)`
  text-align : center;
`

export const StyledCard = ({ title, header, body, links, fullPage }) => {
  // component i use for litteraly everything. overwrite bootstrap card components.
  return (
    <Card className={fullPage ? "full-page" : ""}>

      {header !== undefined &&
        <React.Fragment>
          <Card.Header className="card-header-custom">{header}</Card.Header>
        </React.Fragment>}
      <Card.Body as="div">

        <StyledTitle>{title}</StyledTitle>
        <Card.Text as="div">
          {body}
        </Card.Text>
        {links && links.map((link) => <a key={link} href={link} className="card-link">{link}</a>)}

      </Card.Body>
    </Card>
  )
}

export default StyledCard