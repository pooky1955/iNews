import React from "react"

export const TestableSource = ({ url, headline }) => {

  let fullUrl = '/dashboard/' + encodeURIComponent(url)
  return (
    <div className="testable-source">
      <a href={fullUrl}>{headline}</a>
    </div>
  )
}

export const TestSources = ({ tests }) => {
  console.log(tests)
  const testSources = tests.map((test) => {
    if (test === undefined) {
      
    }
    let url = test[0]
    let headline = test[1]
    let data = { url, headline }
    return <TestableSource {...data} />
  })

  return (
    <div className="test-sources-container mb-4">
      <div className="test-sources-title">Here are some fake news you can test </div>
      <div className="test-links">
        {testSources}
        </div>
    </div>
  )
}


export default TestSources