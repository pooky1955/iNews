import React, { useState } from 'react';
import { BrowserRouter as Router, Redirect, Route, Switch } from "react-router-dom";
import './Appmd.css';
import './Appsm.css';
import './Appxl.css';
import { About } from "./components/About";
import { DashBoardContainer } from "./components/Dashboard";
import { tests } from "./components/data";
import { FrontPage } from "./components/FrontPage";
import { NavBar } from "./components/NavBar";
import { TestSources } from "./components/TestSources";


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

  document.body.style.backgroundColor = backgroundColor



  return (

    <div className="App">
      <NavBar linkUrls={["/", "/about","/demo"]} linkNames={["Home", "About","Demo"]}  />

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
    </div>
  )

}

export default App