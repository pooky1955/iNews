let backendUrl = "http://localhost:5000/"
let aiBackendUrl = "http://localhost:5001/"
const NOFETCH = "Failed to fetch"

export async function postRequest(completeUrl, data) {
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

export async function mediaCheck(mediaName) {

  let endPoint = "mediacheck"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { name: mediaName })
  return json
}

export async function factCheck(headline, keywords) {
  let endPoint = "factcheck"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { headline, keywords })
  return json
}


export async function newsCheck(headline) {

  let endPoint = "detect"
  let completeUrl = `${aiBackendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { headline })
  return json
}

export async function snopeCheck(keywords) {
  let endPoint = "snopecheck"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl, { keywords })
  return json
}


export async function urlExtract(url){
  let endPoint = "extract"
  let completeUrl = `${backendUrl}${endPoint}`
  let json = await postRequest(completeUrl,{url})
  return json
}