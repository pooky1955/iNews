import React from "react"
import { Table, Badge } from "react-bootstrap"
import styled from "styled-components"
const AGREE = 0
const DISAGREE = 1
const DISCUSSES = 2

function* zip(...arrays) {
  for (let i = 0; i < arrays[0].length; i++) {
    let elementsAtI = []
    for (let array of arrays) {
      elementsAtI.push(array[i])
    }
    yield elementsAtI
  }
}

const StanceBadge = ({ stance }) => {
  if (stance === AGREE) {
    return <Badge variant="success" pill>Agree</Badge>
  } else if (stance === DISAGREE) {
    return <Badge variant="danger" pill>Disagree</Badge>

  } else if (stance === DISCUSSES) {
    return <Badge variant="secondary" pill>Discusses</Badge>

  }
}


const StyledLink = styled.a`
  color : black;
  &:hover, &:focus {
    text-decoration : underline;

  }

`

const StancesTable = ({ news }) => {
  // 
  const { publishers, headlines, stances, urls } = news
  let tableHeaders = <thead>
    <tr>
      <th>Publisher</th>
      <th>Headlines</th>
      <th>Stances</th>
      <th>Urls</th>
    </tr>
  </thead>

  let tableRows = []


  for (let [publisher, headline, stance, url] of zip(publishers, headlines, stances, urls)) {
    tableRows.push(
      <tr>
        <td>{publisher}</td>
        <td>{headline}</td>
        <td><StanceBadge stance={stance} /></td>
        <td><StyledLink href={url}>{url}</StyledLink></td>
      </tr>
    )
  }
  return (

    <div style={{overflow : "scroll",width : "90%",}}>
      <h2 style={{ textAlign: "center" }}>Look at the news we found</h2>
      <Table responsive size="sm">
        {tableHeaders}
        {tableRows}
      </Table>
    </div>
  )

}

export default StancesTable