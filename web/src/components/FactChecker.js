import React, { useEffect, useState } from "react"
import { factCheck } from "../util"
import { Badge } from "react-bootstrap"
import styled from "styled-components"
import Loader from "./Loader"
import Error from "./Error"
/*
Disagree : 

*/
const StyledIcon = styled.span`
`

const stancesBadges = [
  "Ok circle",
  "Remove circle icon",
  "Question sign",
]
const stancesDescriptions = [
  "The article is credible",
  "The article is most likely fake news",
  "No information was found on this article"
]

export const FactChecker = ({ headline, keywords }) => {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState({})
  const [isError, setError] = useState(false)
  useEffect(() => {
    (async function () {
      setLoading(true)
      try {
        let data = await factCheck(headline, keywords)
        setData(data)
        setError(false)
      } catch (exception) {
        console.error(exception)
        setError(true)
      }
      setLoading(false)
    })()

  }, [])
  if (isError) {
    return <Error actionString="fact checking"></Error>
  }
  if (loading) {
    return <Loader text="Fact checking"></Loader>
  }
  return (
    <div>
      <p>
        Hello there! We have not yet implemented <code>FactChecker.js</code>
      </p>
    </div>
  )

}
export default FactChecker