import { snopeCheck } from "../util"
import React, { useState, useEffect } from "react"
import { Loader } from "./Loader"
import { Error } from "./Error"
import {StyledCard} from "./Card"

export const SnopesChecker = ({ articleKeywords, setRating }) => {
  let [loading, setLoading] = useState(false)
  let [isError, setError] = useState(false)
  let [hasData, setHasData] = useState(false)
  let [data, setData] = useState({})
  useEffect(() => {
    (async function () {
      setLoading(true)
      try {
        let data = await snopeCheck(articleKeywords)
        if (data.hasData){
          setData(data)
          setHasData(true)
        }
        setError(false)
      } catch (exception) {
        console.error(exception)
        setError(true)
      }
      setLoading(false)
    })()

  }, [])


  
  if (isError) {
    const header = "Fact checkers"
    const body = <Error actionString="searching Snopes"></Error>
    const cardProps = {header,body}
    return <StyledCard {...cardProps}/>
  }
  if (loading) {
    const header = "Fact checkers"
    const body = <Loader text="Searching Snopes"></Loader>
    const cardProps = {header,body}
    return <StyledCard {...cardProps}/>
  }

  if (hasData) {

    const { snippet, rating, url } = data
    setRating(rating)

    const title = `Rated as ${rating[0]}`
    const body = snippet
    const header = "Fact checkers"
    const links = [url]

    const cardProps = {title,body,header,links}

    return <StyledCard {...cardProps}/>
  } else {

    const body = "No fact checking websites have verified the article"
    const header = "Fact checkers"
    
    const cardProps = {body,header}
    return <StyledCard {...cardProps}/>
  }

}
export default SnopesChecker