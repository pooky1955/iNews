import React, { useState } from "react"
import styled from "styled-components"
import {Loader} from "./Loader.js"
import { StyledCard } from "./Card"

function* zip(...arrays) {
  for (let i = 0; i < arrays[0].length; i++) {
    let elementsAtI = []
    for (let array of arrays) {
      elementsAtI.push(array[i])
    }
    yield elementsAtI
  }
}

function* enumerate(iterable) {
  let counter = 0
  for (let object of iterable) {
    yield [counter, object]
    counter++
  }
}


function shorten(headline, maxWords) {
  let shortened = headline.split(" ").slice(0, maxWords).join(" ")
  return shortened
}
const allStancesCaps = ["Agree","Disagree","Discuss"]
const allStances = ["agree", "disagree", "discuss"]
const StanceChanger = ({ updateStance }) => {
  let stancesButton = allStancesCaps.map((stance, index) => <button className={`btn change-stance-btn ${stance.toLowerCase()}-btn`} onClick={() => {
    updateStance(index)
  }}>{stance}</button>)
  return (
    <React.Fragment>
      <span className="change-stance-text">Wrongly classified? Help us change it!</span>
      <div className = "stance-changer-button">
      {stancesButton}
      </div>
    </React.Fragment>
  )
}

export const StancesTable = ({ news, updateStances, hasData }) => {
  // 
  const header = "Factual News Search Table View"
  if (news === undefined) {
    const body = <Loader text="Waiting for Factual News Search"></Loader>
    const cardProps = { body, header }
    return <StyledCard {...cardProps} />
  } else {
    const { publishers, headlines, stances, urls } = news
    let tableRows = []
    //sorry ha i did too much python and just love to use zip and enumerate :)
    for (let [index, [publisher, headline, stance, url]] of enumerate(zip(publishers, headlines, stances, urls))) {
      let shortened = shorten(headline, 10) + " [...]"
      let stanceText = allStances[stance]
      let stanceCapsText = allStancesCaps[stance]
      tableRows.push(
        <div className={[stanceText, "stance-row"].join(' ')}>
          <div className="side-banner"> </div>
          <div className="right-side-banner">
            <div>
              <div className = "stance-headline">
                <span>{shortened} </span> <span className="stance-publisher">by {publisher.toUpperCase()}</span>
              </div>
              <div className = "stance-classification">
                Stance detected : <span className={[`${stanceText}-badge`, "stance-badge"].join(" ")}>{stanceCapsText}</span>
              </div>
              <div className = "stance-changer">
                <StanceChanger updateStance={(newStance) => {
                  debugger
                  updateStances(index, newStance)
                }} />
              </div>
              <a href={url} className="btn link-btn" target="_blank">Visit website</a>
            </div>
          </div>
        </div>
      )
    }
    const body = (<div className="stance-table">
      {tableRows}
    </div>)
    const cardProps = { body, header }
    return (<StyledCard {...cardProps} />)

  }
}

export default StancesTable