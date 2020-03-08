let iNewsUrl = "localhost:5000/mediacheck"
let backendUrl = "http://localhost:5000/"
let aiBackendUrl = "http://localhost:5001/"
const NOFETCH = "Failed to fetch"
console.log("chrome extension go!")

let INewsData = {}
let webPageUrl = "http://localhost:3000"

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

function closePopup() {
  let popupElem = document.querySelector(".inews-popup")
  popupElem.parentElement.removeChild(popupElem)
}

function preparePopup({bottom,left}){
  let bodyRect = document.body.getBoundingClientRect()

  let INewsPopup = document.createElement("div")
  INewsPopup.style.position = "absolute"
  INewsPopup.style.top = bottom - bodyRect.y + "px"
  INewsPopup.style.left = left - bodyRect.x + "px"
  INewsPopup.classList.add("inews-popup")
  INewsData.popup = INewsPopup
  document.body.appendChild(INewsPopup)
}

function showLoader(){
  const INewsPopup = INewsData.popup
  INewsPopup.innerHTML = `
    <div class = "inews-popup-title"> Analyzing source ... </div>
  `
}

function showHasData({credibility,category,url,name},newsUrl){
  const INewsPopup = INewsData.popup
  let popupTitle = credibility ? "The source seems credible" : "The source is not credible"
  let encodedNewsUrl = encodeURIComponent(newsUrl)
  INewsPopup.innerHTML = `
    <div class = "inews-popup-title"> ${popupTitle} </div>
    <div class = "inews-popup-source">${name} is classified as ${category}.<br/> <a href = "${url}" class="inews-popup-link">Learn more</a> </div>
    <a class = "inews-popup-details" href="${webPageUrl}/dashboard/${encodedNewsUrl}">Perform a deeper analysis</a>
    <div class = "inews-popup-xmark">&times;</div>
  `

}
function showNoData(newsUrl){
  const INewsPopup = INewsData.popup
  let encodedNewsUrl = encodeURIComponent(newsUrl)
  INewsPopup.innerHTML = `
    <div class = "inews-popup-title"> Source not found  </div>
    <a class = "inews-popup-details" href="${webPageUrl}/dashboard/${encodedNewsUrl}">Perform a deeper analysis</a>
    <div class = "inews-popup-xmark">&times;</div>
  `
}
async function createToolTip(boundingRect,url) {
  //i want to make a popup such that the upper left corner of the popup is at the bottom left corner, so basically its kinda like a rectangle directly underneath the link
  preparePopup(boundingRect)
  showLoader()
  let data = await mediaCheck(url)  
  console.log(data)
  
  if (data.hasData){
    showHasData(data,url)
  } else {
    showNoData()
  }
  let elem = document.querySelector(".inews-popup-xmark")
  console.log(elem)
  elem.addEventListener("click",()=>{
    closePopup()
  })

}

chrome.runtime.onMessage.addListener(gotMessage)
function gotMessage(message, sender, sendResponse) {
  console.log({ message, sender, sendResponse })
  const element = INewsData.selected
  console.log("retrieved element", element)
  let boundingRect = element.getBoundingClientRect()
  const {url} = message
  createToolTip(boundingRect,url)
}

function loadStyleSheet() {
  let cssUrl = chrome.extension.getURL("style.css")
  let link = document.createElement("link")
  link.rel = "stylesheet"
  link.type = "text/css"
  link.href = cssUrl
  link.onload = "alert('loaded stylesheet')"
  document.head.appendChild(link)
}


window.oncontextmenu = (e, b) => {
  console.log(e)
  console.log(b)
  let element = e.target
  console.log("selected element", element)
  INewsData.selected = element
}


document.body.onload = function () {
  loadStyleSheet()
  console.log("Load style sheet")
}