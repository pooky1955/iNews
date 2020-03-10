import React, { useEffect } from "react"
import styled from "styled-components"
import { NewsChecker } from "./NewsChecker"
import { SnopesChecker } from "./SnopesChecker"
import { urlExtract } from "../util"
import { SourceChecker } from "./SourceChecker"
import { Redirect } from "react-router-dom"
import { useState } from "react"
import { StatisticsPanel } from "./Statistics"
import { Loader } from "./Loader"
import { Error } from "./Error"
import { ArticleClass, standardize } from "./ArticleClass"
import { QuestionableSource } from "./QuestionnableSource"
import {StyledCard} from "./Card"
import StancesTable from "./StancesTable"

const size = {
  mobileS: '320px',
  mobileM: '375px',
  mobileL: '425px',
  tablet: '768px',
  laptop: '1024px',
  laptopL: '1440px',
  desktop: '2560px'
}
export const device = {
  mobileS: `(max-width: ${size.mobileS})`,
  mobileM: `(max-width: ${size.mobileM})`,
  mobileL: `(max-width: ${size.mobileL})`,
  tablet: `(max-width: ${size.tablet})`,
  laptop: `(max-width: ${size.laptop})`,
  laptopL: `(max-width: ${size.laptopL})`,
  desktop: `(max-width: ${size.desktop})`,
  desktopL: `(max-width: ${size.desktop})`
};
function extractHost(url) {
  let splittedHttp = url.split("//")[1]
  for (let segment of splittedHttp.split(".")) {
    if (segment === "www") {
      continue
    } else {
      return segment
    }
  }
}
export const DashBoardContainer = ({ encodedUrl }) => {
  let url = decodeURIComponent(encodedUrl)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(undefined)
  useEffect(() => {
    (async function () {
      let mediaName = extractHost(url)
      try {
        setLoading(true)
        let response = await urlExtract(url)
        let data = Object.assign({}, response, { mediaName })
        setError(false)
        setData(data)
      } catch (exception) {
        setError(true)
      }
      setLoading(false)
    })()
  }, [])
  if (loading) {
    const body = <Loader text="Extracting info on article url" />
    const cardProps = { body }
    return <StyledCard {...cardProps} fullPage/>
  } else if (error) {
    const body = <Error actionString="extracting info on article url" />
    const cardProps = { body }
    return <StyledCard {...cardProps} fullPage/>
  }
  if (data !== undefined) {
    return <DashBoard {...data} />
  } else {
    return ""
  }
}



const QUESTIONABLESOURCE = "questionablesource"

export const DashBoard = ({ headline, articleKeywords, mediaName }) => {


  const [credibility, setCredibility] = useState(undefined)
  const [newsData, setNewsData] = useState(undefined)
  const [sourceCategory, setSourceCategory] = useState(undefined)
  const [rating, setRating] = useState(undefined)

  if (!headline || !articleKeywords || !mediaName) {
    return <Redirect to="/"></Redirect>
  }

  let articleProps = { credibility, rating, sourceCategory }
  // if (sourceCategory !== undefined) {
  //   let standardizedSourceCategory = standardize(sourceCategory)
  //   if (standardizedSourceCategory === QUESTIONABLESOURCE) {
  //     return <QuestionableSource />
  //   }
  // }


  return (
    <div className="dashboard-container">
      <div className="dashboard-top-container">
        <div className="dashboard-side-container">
          <ArticleClass {...articleProps} />
          <StatisticsPanel {...articleProps} />
          <NewsChecker headline={headline} setCredibility={(credibility) => {
            setCredibility(credibility)
          }} setData={(news) => { setNewsData(news) }} data={newsData}></NewsChecker>

        </div>
        <div className="dashboard-side-container">
          <SnopesChecker articleKeywords={articleKeywords} setRating={(ratings) => {
            setRating(ratings[0])
          }} />
          <SourceChecker source={mediaName} setSourceCategory={(sourceCategory) => {
            setSourceCategory(sourceCategory)
          }}></SourceChecker>
        </div>
      </div>
      <div className="dashboard-bottom-container">
        <StancesTable news={newsData} updateStances={(index, newStance) => {
          let { stances, ...rest } = newsData
          let newStances = stances.slice() // copies array
          newStances[index] = newStance
          let newNewsData = { stances: newStances, ...rest }
          setNewsData(newNewsData)
        }}></StancesTable>
      </div>
    </div>
  )
}
export default DashBoard