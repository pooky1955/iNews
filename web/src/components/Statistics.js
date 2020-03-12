import React from "react"
import { Card } from "react-bootstrap"
import {StyledCard} from "./Card"
import styled from "styled-components"
import Loader from "./Loader"

const Boldened = styled.span`
  font-weight : 800
`

const CredibilityContainer = ({ credibility }) => {


  if (credibility < 60) {
    return (
      <div>
        Credibility :  <Boldened style={{ color: "red" }}>{credibility}%</Boldened>
      </div>
    )
  } else {
    return (
      <div>
        Credibility : <Boldened style={{ color: "green" }}>{credibility}%</Boldened>
      </div>
    )
  }
}

const DefaultContainer = ({ children, defaultValue = "", value }) => {
  if (value !== false && value !== undefined) {
    return (
      <React.Fragment>
        {children}
      </React.Fragment>
    )
  } else {
    return defaultValue
  }
}


export const StatisticsPanel = ({ credibility, rating, sourceCategory }) => {
  const header = "iNews Statistics"
  if (!credibility && !rating && !sourceCategory) {
    const body =  <Loader text="Waiting for results to show up"></Loader>
    const cardProps = {body,header}
    return <StyledCard {...cardProps}/>
  }
  return (

    <Card className = "statistics-panel">
      <Card.Header>iNews Statistics</Card.Header>
      <Card.Body className="d-flex flex-row align-items-center flex-wrap" style={{ justifyContent: "space-evenly" }}>
        <DefaultContainer value={credibility}>
          <CredibilityContainer credibility={credibility} />
        </DefaultContainer>

        <DefaultContainer value={rating} >
          <div>
            Rated on Snopes as : <Boldened>{rating}</Boldened>
          </div>
        </DefaultContainer>

        <DefaultContainer value={sourceCategory !== undefined && sourceCategory !== "__nosource__"}>
          <div>
            Source classified as : <Boldened>{sourceCategory}</Boldened>
          </div>
        </DefaultContainer>
      </Card.Body>
    </Card>
  )
}