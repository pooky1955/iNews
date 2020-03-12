import React from "react"
import fakeIcon from "./images/false.png"
import trueIcon from "./images/true.png"
import {Loader} from "./Loader"
import {StyledCard} from "./Card.js"

const SATIRE = "satire"
const NOTRELIABLE = ["conspiracypseudoscience", "questionablesource"]
const SNOPEFALSE = ["mostlyfalse", "false", "miscaptioned", "misattributed", "scam","labeledsatire"]

function split(string) {
  let patt = /[\s-]/ig
  let splitted = string.split(patt)
  return splitted
}

export function standardize(source) {
  let lowered = source.toLowerCase()
  let noSpaces = split(lowered).join("")
  return noSpaces
}

function partOf(array, targetEl) {
  for (let el of array) {
    if (el === targetEl) {
      return true
    }
  }
  return false
}

export const ArticleClass = ({ sourceCategory, rating, credibility }) => {
  
  const header = "iNews Results"
  // just need one thing and credibility
  if ((!sourceCategory || !rating) && !credibility){
    const body = <Loader text = "Waiting for results"/>
    const cardProps = {body,header}
    return <StyledCard {...cardProps}/>
  }
  
  let [isFake, causes] = checkFake(credibility, rating, sourceCategory)
  if (isFake) {
    // fake news body
    const body  = (
      <div className="result">
        <img src={fakeIcon}  alt = "fake-news-icon" className="result-icon mr-4" />

        <div>
          <div className="result-label">This is a fake news!</div>
          <div className="result-explanation">
            {causes.map(cause => <div className="result-explanation-list-element" key={cause}>{cause}</div>)}
          </div>
        </div>
      </div>
    )
    const cardProps = {body,header}
    return <StyledCard {...cardProps}/>
  } else {
    // true news body
    const body =  (
      <div className="result">
        <img src={trueIcon} alt = "true-news-icon" className="result-icon mr-4" />

        <div>
          <div className="result-label">This news is true!</div>
          <div className="result-explanation">
            {causes.map(cause => <div className="result-explanation-list-element">{cause}</div>)}
          </div>
        </div>
      </div>
    )
    const cardProps = {body, header}
    return <StyledCard {...cardProps}/>
  }

}

function checkFake(credibility, rating, sourceCategory) {
  let causes = []
  let isFake = false
  if (sourceCategory !== undefined && sourceCategory !== "__nosource__") {
    let standardizedSourceCategory = standardize(sourceCategory)
    if (standardizedSourceCategory === SATIRE) {
      isFake = true
      causes.push("Source is a satire")
    }
    if (partOf(NOTRELIABLE, standardizedSourceCategory)) {
      isFake = true
      causes.push("Source is not reliable")
    }
  }
  if (rating !== undefined) {
    let standardizedRating = standardize(rating)
    
    if (partOf(SNOPEFALSE, standardizedRating)) {
      isFake = true
      causes.push("Fact-Checking websites have deemed it false")
    }
  }

  if (isFinite(credibility)) {
    let threshold = 60
    if (credibility < threshold) {
      isFake = true
      causes.push(`More than ${100 - threshold}% of the media disagree with this article`)
    }
  }
  if (!isFake){
    causes = ["This article has passed all the tests"]
  }
  return [isFake, causes]
}


export default ArticleClass