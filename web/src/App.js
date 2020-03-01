import React, {useState} from 'react';
import { BrowserRouter as Router, Route, Switch , Redirect} from "react-router-dom";
import './Appsm.css';
import './Appmd.css'
import './Appxl.css';
import { DashBoardContainer } from "./components/Dashboard";
import styled from "styled-components"
import { NavBar } from "./components/NavBar"
import {About} from "./components/About"
import { FrontPage } from "./components/FrontPage";
import {tests} from "./components/data"
import {TestSources} from "./components/TestSources"
import {LanguageProvider} from "./LanguageContext"


export function goToPage(pageNumber) {
  window.scrollTo(0, pageNumber * window.innerHeight)
}

export const App = () => {
  let backgroundColor;
  if (window.location.pathname.startsWith("/dashboard")){
    backgroundColor = "whitesmoke"
  } else {
    backgroundColor = "white"
  }

const StyledBackgroundDiv = styled.div`
    background-color : ${backgroundColor}
  `

  const [language,setLanguage] = useState("en")


  return (

<LanguageProvider value = {language}>
    <StyledBackgroundDiv className="App">
      <NavBar linkUrls={["/", "/about","/demo"]} linkNames={["Home", "About","Demo"]} updateLanguage = {(language)=>{setLanguage(language)}} />

      <div className="content">
        <Router>
          <Switch>
          <Route path = "/about" exact component = {About}/>
          <Route path = "/demo" exact render = {()=><TestSources tests = {tests}/>}/>
            <Route path="/" exact component={FrontPage} />
            <Route path="/dashboard/:encodedUrl" render={props =>
              <DashBoardContainer {...props.match.params} />
            } />
          <Redirect to = "/"/>
          </Switch>
        </Router>
      </div>
    </StyledBackgroundDiv>
</LanguageProvider>
  )

}

export default App