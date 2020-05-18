document.addEventListener('init', function(evt){
    chrome.runtime.sendMessage({type:"init"}, function(response){

    });
}, false);

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
    console.log(message);
})