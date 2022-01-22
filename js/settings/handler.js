document.addEventListener("DOMContentLoaded",function(dcle) {
    chrome.storage.sync.get(['blocked'], function(result) {
        console.log(result.blocked)
    }); 

    var input_box = $('#In')
    input_box.keydown(function (keyevent) {
        if (keyevent.keyCode === 13) {
            chrome.storage.sync
        } 
    })
}); 