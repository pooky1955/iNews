import React, { useEffect, useState } from "react"
import { Doughnut } from "react-chartjs-2"
import { newsCheck } from "../util"
import { StyledCard } from "./Card"
import Error from "./Error"
import { Loader } from "./Loader"
function getCounts(stances) {
  let counts = [0, 0, 0]
  for (let stance of stances) {
    counts[stance] += 1
  }
  return counts
}


export const NewsChecker = ({ headline, setCredibility, setData, data }) => {
  const [isError, setError] = useState(false)
  const [loading, setLoading] = useState(false)
  const [hasData, setHasData] = useState(false)

  useEffect(() => {
    // Code to fetch stances count
    (async function () {
      setLoading(true)
      try {
        let newData = await newsCheck(headline)
        setError(false)
        setHasData(true)
        setData(newData)
      } catch (exception) {
        console.error(exception)
        setError(true)
      }
      setLoading(false)
    })()
  }, [])

  const header = "Factual News Search"
  if (isError) {
    // Show error
    const body = <Error actionString="searching Factual News Search"></Error>
    const cardProps = { body, header }
    return <StyledCard {...cardProps} />
  }
  if (loading) {
    // Display loader
    const body = <Loader text="Searching Factual News Search"></Loader>
    const cardProps = { body, header }
    return <StyledCard {...cardProps} />
  }
  if (hasData) {
    // Should display the agree metrics and disagree beautiful chart plot
    const { stances } = data

    function percent(count) {
      return Math.round(100 * count / (agreeCount + disagreeCount + discussCount))
    }

    const [agreeCount, disagreeCount, discussCount] = getCounts(stances)
    let credibility = percent(agreeCount)
    setCredibility(credibility)

    const body = (
      <div className="metrics-display">
        <div className="agree-metrics">
          <div className="metrics-percentage">{percent(agreeCount)}%</div>
          <div className="metrics-count">{agreeCount} news</div>
          <div className = "metrics-category">Agree</div>
        </div>
        <div className="disagree-metrics">
          <div className="metrics-percentage">{percent(disagreeCount)}%</div>
          <div className="metrics-count">{disagreeCount} news</div>
          <div className = "metrics-category">Disagree</div>
        </div>
        <div className="discuss-metrics">
          <div className="metrics-percentage">{percent(discussCount)}%</div>
          <div className="metrics-count">{discussCount} news</div>
          <div className = "metrics-category">Discuss</div>
        </div>
      </div>
    )


    const title = "Here's what the media thinks"
    const cardProps = { title, header, body }

    return <StyledCard {...cardProps} />
  } else {
    // No data found
    const body = "No similar news were found online"
    const cardProps = { body, header }
    return <StyledCard {...cardProps} />

  }
}
export default NewsChecker