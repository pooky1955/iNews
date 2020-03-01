import React from 'react'
import styled from "styled-components"

export const Page = (props) => {
  const { background, invisible,center,padded } = props
  let FullPage = styled.div`
  width : 100vw;
  height : 100vh;
  position : relative;
  background : ${background};
  display : ${invisible? "none":"block"}
  `

  if (center){
    FullPage = styled(FullPage)`
      display : flex;
      align-items : center;
      flex-direction : column;
      justify-content : center;
    `
  }

  if (padded){
    FullPage = styled(FullPage)`
      margin : 5vmin;
    `
  }
  
  return (

      <FullPage>
        {props.children}
      </FullPage>
    
  )
}
export default Page