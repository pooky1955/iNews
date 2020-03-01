import React, { useState, useEffect } from "react"
import { newsCheck } from "../util"
import Error from "./Error"
import { Doughnut } from "react-chartjs-2"
import { Loader } from "./Loader"
import { StyledCard } from "./Card"


let AGREE = 0
let DISAGREE = 1
let DISCUSSES = 2

let colors = {
  agree: {
    normal: "hsl(82, 57%, 61%)",
    hover: "hsl(82,87%,61%)",
  },
  disagree: {
    normal: "hsl(9, 100%, 61%)",
    hover: "hsl(9, 100%, 61%)",
  },
  neutral: {
    normal: "hsl(32, 100%, 77%)",
    hover: "hsl(32,110%,77%)"
  },
}

const StancesPieChart = ({ agreeCount, disagreeCount }) => {
  const data = {
    labels: [
      "Agree",
      "Disagree",
    ],
    datasets: [{
      data: [agreeCount, disagreeCount],
      backgroundColor: [
        colors.agree.normal,
        colors.disagree.normal,

      ],
      hoverBackgroundColor: [
        colors.agree.hover,
        colors.disagree.hover,
      ],
      borderAlign: 'inner'
    }]
  }
  return (
    <article className="canvas-container" style={{width: "calc(50px + 60vw)",display : "flex", alignItems : "center",flexDirection : "column" }}>
      <Doughnut data={data} ></Doughnut>
    </article>
  )
}

function getCounts(stances) {
  let counts = [0, 0, 0]
  for (let stance of stances) {
    counts[stance] += 1
  }
  return counts
}

function aggregateData(data){
  let aggregated = []
  const {publishers,urls,stances} = data
  for (let i = 0 ; i < stances.length; i++){
    let publisher = publishers[i]
    let url = urls[i]
    let stance = stances[i]
    let el =  { publisher, url , stance}
    aggregated.push(el)
  }
  return aggregated
}

export const NewsChecker = ({ headline, setCredibility }) => {
  const [isError, setError] = useState(false)
  const [loading, setLoading] = useState(false)
  const [hasData, setHasData] = useState(false)
  const [data, setData] = useState({})

  useEffect(() => {

    (async function () {
      setLoading(true)
      try {
        let data = await newsCheck(headline)
        setError(false)
        setHasData(true)
        setData(data)
      } catch (exception) {
        console.error(exception)
        setError(true)
      }
      setLoading(false)
    })()
  }, [])

  if (isError) {
    return <div><Error actionString="searching Google News"></Error></div>
  }
  if (loading) {
    return (
      <Loader text="Searching Google News"></Loader>
    )
  }
  if (hasData) {
    const { stances,urls} = data
    
    const [agreeCount, disagreeCount,_] = getCounts(stances)
    const aggregatedData = aggregateData(data)
    let agreeUrls = aggregatedData.filter((row)=>row.stance === AGREE).map((row)=>row.url)
    let disagreeUrls = aggregatedData.filter((row)=>row.stance === DISAGREE).map((row)=> row.url)

    let agreePublishers = aggregatedData.filter((row)=>row.stance === AGREE).map((row)=>row.publisher)
    let disagreePublishers = aggregatedData.filter((row)=>row.stance === DISAGREE).map((row)=>row.publisher)

    let agreeHeadlines = aggregatedData.filter((row)=>row.stance === AGREE).map((row)=>row.headline)
    let disagreeHeadlines = aggregatedData.filter((row)=>row.stance === DISAGREE).map((row)=>row.headline)
    
    debugger

    let credibility = Math.round(100 * agreeCount / (agreeCount + disagreeCount))
    setCredibility(credibility)
    const body = (<div className = "chart-container d-flex align-items-center justify-content-center flex-column">
      <StancesPieChart {...{ agreeCount, disagreeCount }}></StancesPieChart>
    </div>)
    const title = "Here's what the media thinks"
    const header = "Google News"
    const cardProps = {title, header, body}
    return <StyledCard {...cardProps}/>
  }
  return <div></div>
}
export default NewsChecker