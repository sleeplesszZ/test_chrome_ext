let port = null;
let hostname = "com.my_company.example"
let g_TabId = null;
let g_WindowId = null;

chrome.runtime.onMessage.addListener(function(message, sender, response){
    let tabId = sender.tab.id;
    let windowId = sender.windowId;
    if (message.type == 'init') {
        connect();
        g_TabId = tabId;
    }
    else{
        if (null == g_TabId) {
            
        }
        else if (tabId == g_TabId){

        }
        else{
            console.log('current tabId is different from ' + g_TabId);
        }
    }
})

chrome.tabs.onRemoved.addListener(function(id){
    if (id == g_TabId){
        port.PostMessage({msg:{function:'close'}});
    }
});

function getCurrentTabId(msg){
    chrome.tabs.query({active:true, currentWindow: true}, function(tabs){
        g_TabId = tabs.length ? tabs[0].id : null;
    });
};

function connect() {
    port = chrome.runtime.connectNative(hostname);
    port.onMessage.addListener(onNativeMessage);
    port.onDisconnect.addListener(onDisconnected);
 } 


function onNativeMessage(message) {
    SendMsgToTab(message);
}
  
function onDisconnected() {
    console.log('onDisconnect  ' + chrome.runtime.lastError.message);
    g_TabId = null;
    port = null;
}

function SendMsgToTab(msg){
    chrome.tabs.sendMessage(g_TabId, msg);
}