let iNewsUrl = "localhost:5000/mediacheck"
let backendUrl = "http://localhost:5000/"
let aiBackendUrl = "http://localhost:5001/"
const NOFETCH = "Failed to fetch"
console.log("chrome extension go?")

async function postRequest(completeUrl, data) {
  let resp = await fetch(completeUrl, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  if (resp.ok) {
    let json = await resp.json()
    return json
  } else {
    throw NOFETCH
  }
}

async function mediaCheck(mediaName) {

  let endPoint = "mediacheck"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { name: mediaName })
  return json
}

async function urlExtract(url) {
  let endPoint = "extract"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { url })
  return json
}

async function verifyUrl(e){
  let element = e.currentTarget
  if (element.dataset.checkedByINews){
    return
  }
  element.dataset.checkedByINews = true
  let url = element.attributes["href"].value
  
  if (!url.startsWith("http") && !url.startsWith("www")){
    return
  }
  console.log(element)
  console.log(url)
  if (url === undefined){
    return
  } 
  let json = await mediaCheck(url)
  console.log(json)
  const {credibility, category, mbfcUrl,name, hasData} = json
  if (!hasData){
    src = "images/unknown.png"
  } else if (credibility){
    src = "images/credible.png"
    
  } else {
    src = "images/notcredible.png"
  }
  let completeSrc = chrome.extension.getURL(src)
  let categoryNode = hasData ? `[${category}]` : ''
  element.innerHTML = `<img src = "${completeSrc}" style = "height:1em;"/>` + categoryNode + element.innerHTML
}


function setup() {
  let shouldContinue = confirm("continue using iNews")
  if (!shouldContinue){
    return
  }
  for (let aTag of document.querySelectorAll("a")) {
    aTag.addEventListener("mouseover",verifyUrl)
  }
}


document.body.onload = setup