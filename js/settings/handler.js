document.addEventListener("DOMContentLoaded", function (  ) {
    // Laeb blokeeritud asjad
    chrome.storage.sync.get(['blocked'], function(result) {
        if (result != undefined) {
            result.blocked.forEach(element => {
                $('tbody').append(`<tr><td>${element}  <button>X</button></td></tr>`)
            });    
        }
    }); 

    // Asjade lisamine funtksionaalsus
    var input_box = $('#In')
    input_box.keydown(function (keyevent) {
        if (keyevent.keyCode === 13) {
            chrome.storage.sync.get(['blocked'], function (result) {
                let current_list = result.blocked
                let inpvalue = input_box.val()
                current_list.push(inpvalue)
                chrome.storage.sync.set({blocked: current_list})
                $('tbody').append(`<tr><td>${inpvalue}  <button>X</button></td></tr>`)
            })
        } 
    })

    // Asjade eemaldamise funtks
    //console.log($('#Delete'))

}); 