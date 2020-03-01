import React from "react"
import frenchIcon from "./images/french.png"
import englishIcon from "./images/english.png"

const LANGUAGES = [
  ["fr",frenchIcon],
  ["en",englishIcon]
]


function* zip(...lists){
  for (let i = 0 ; i < lists[0].length; i++){
    let yieldedArray = []
    for (let j = 0 ; j < lists.length; j++){
      yieldedArray[j] = lists[j][i]
    }
    yield yieldedArray 
  }
}
export const NavBar = ({ linkNames, linkUrls ,updateLanguage}) => {
  let linkComponents = []
  for (let [linkName,linkUrl] of zip(linkNames,linkUrls)){
    let linkComponent = <div><a className="main-nav-link" href = {linkUrl}>{linkName}</a></div>
    linkComponents.push(linkComponent)
  }

  let languagesComponents = LANGUAGES.map((language)=><img onClick = {()=>{updateLanguage(language[0])}} src = {language[1]} className = "nav-language-icon"/>)
  
  return (
    <nav className = "main-nav">
      <div className = "nav-brand">
        iNews
      </div>
      <div className = "nav-links">
      {linkComponents}    
        {/* {languagesComponents} */}
      </div>
    </nav>
  )
}

export default NavBar