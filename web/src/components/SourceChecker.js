import React, { useState, useEffect } from "react"
import { StyledCard } from "./Card"
import { mediaCheck } from "../util"
import { Error } from "./Error"
import { Loader } from "./Loader"

function isAllCaps(text) {
  return text.toUpperCase() === text
}

function capitalize(word) {
  let chars = word.toLowerCase().split("")
  let capitalLetter = chars[0].toUpperCase()
  let rest = chars.slice(1, chars.length).join('')
  return capitalLetter + rest
}

function extractSourceCategory(text) {
  let category = []

  for (let word of text.split(" ")) {
    if (isAllCaps(word) && word.length > 1) {
      category.push(capitalize(word))
    } else {
      break
    }
  }
  return category.join(' ')
}






export const SourceChecker = ({ source, setSourceCategory }) => {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState({})
  const [isError, setError] = useState(false)
  const [hasData, setHasData] = useState(false)
  useEffect(() => {
    (async function () {
      setLoading(true)
      try {
        let mediaInfo = await mediaCheck(source)
        setHasData(true)
        setData(mediaInfo)
        setError(false)
      }
      catch (exception) {
        console.error(exception)
        setError(true)
      }
      setLoading(false)
    })()
  }, [])
  if (isError) {
    let header = "Media Bias Fact Check"
    const body = <Error actionString="searching on Media Bias Fact Check"></Error>
    const cardProps = { header, body }
    return <StyledCard {...cardProps} />
  }
  if (loading) {
    let header = "Media Bias Fact Check"
    const body = <Loader text="Searching on Media Bias Fact Check"></Loader>
    const cardProps = { header, body }
    return <StyledCard {...cardProps} />
  }
  if (hasData) {
    
    // const header = "Media Bias Fact Check"
    let header = "Media Bias Fact Check"
    const { description, url } = data
    if (description === undefined || url === undefined) {
      const body = "This source wasn't registered in Media Bias Fact Check"
      const cardProps = { body, header }
      return <StyledCard {...cardProps} />

    }
    let category = extractSourceCategory(description)
    let shortenedDescription = shortenDescription(description)

    setSourceCategory(category)

    const body = shortenedDescription
    const title = category
    const links = [url]

    const cardProps = { body, header, title, links }
    return (<StyledCard {...cardProps}></StyledCard>)

  } else {
    return <div></div>

  }
}

function shortenDescription(description) {
  let shortenedList = []
  for (let word of description.split(" ")) {
    if (isAllCaps(word) && word.length > 1) {
      continue
    }
    shortenedList.push(word)

  }
  let shortened = shortenedList.join(" ")
  let firstSentence = shortened.split(".")[0] + "."
  return firstSentence

}
export default SourceChecker