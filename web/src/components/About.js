import React from "react"
import icon from "./images/icon.png"
export const About = () => {
  //Code for making the about tab
  return (
    <div className="about-container">
      <div className="about-title">iNews</div>
      <div className="about-description">
        iNews is a fake news detector based on machine learning and NLP.
        It combines stance detection, scraping fact checking websites, and verifying the source of the article.
        iNews was originally made for the Expo-Sciences 2020.
      </div>

      <div className="about-mascot-container">
        <img alt="iNews mascot" src={icon} className="about-icon" />
      </div>

    </div>
  )
}
export default About