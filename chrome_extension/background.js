console.log("Chrome Extension iNews is running.")

function onClickHandler(info,tab){
  console.log("HELLO?")
  console.log(tab)
  let url = info.linkUrl
  console.log(url,info)
  let msg = {
    url, info
  }
  chrome.tabs.sendMessage(tab.id,msg)
}


chrome.runtime.onInstalled.addListener(()=>{
  let context = "link"
  let title = "iNews"
  let id = chrome.contextMenus.create({title,contexts : [context],id : `context-${context}`})
})

chrome.contextMenus.onClicked.addListener(onClickHandler)

