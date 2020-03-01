import React from "react"
import falseIcon from "./images/false.png"
import dangerIcon from "./images/danger.png"

export const QuestionableSource = () => {
  return (
    <div className="questionable-source-container">
      <div className="fake-news-container mt-4">
        <img src={falseIcon} className="result-icon mr-4"  alt = "fake-news-icon"/>
        <div className="questionable-source-label result-label">This is a fake news</div>
      </div>
      <div className="danger-container mt-4">
        <img src={dangerIcon} className="result-icon mr-4" alt = "danger-icon"/>
        <div className="questionable-source-description ">Careful! Always check the source of an article! The article was from a questionable source according to Media Bias Fact Check.<br /></div>
      </div>
      <div className="questionable-source-quote mt-4">
        A questionable source exhibits one or more of the following: extreme bias, consistent promotion of propaganda/conspiracies, poor or no sourcing to credible information, a complete lack of transparency and/or is fake news.
        </div>
        <div className = "questionable-source-author mt-2"><a href = "https://mediabiasfactcheck.com/fake-news/">- Media Bias Fact Check </a></div>
    </div>
  )
}

export default QuestionableSource