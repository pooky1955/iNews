import React from "react"
import frenchIcon from "./images/french.png"
import englishIcon from "./images/english.png"

function* zip(...lists){
  for (let i = 0 ; i < lists[0].length; i++){
    let yieldedArray = []
    for (let j = 0 ; j < lists.length; j++){
      yieldedArray[j] = lists[j][i]
    }
    yield yieldedArray 
  }
}
export const NavBar = ({ linkNames, linkUrls }) => {
  let linkComponents = []
  for (let [linkName,linkUrl] of zip(linkNames,linkUrls)){
    let linkComponent = <div key={linkUrl}><a className="main-nav-link" href = {linkUrl}>{linkName}</a></div>
    linkComponents.push(linkComponent)
  }

  
  return (
    <nav className = "main-nav">
      <div className = "nav-brand">
        iNews
      </div>
      <div className = "nav-links">
      {linkComponents}    
      </div>
    </nav>
  )
}

export default NavBar