var current_list = []

document.addEventListener("DOMContentLoaded", function (  ) {
    // Laeb blokeeritud asjad
    chrome.storage.sync.get(['blocked'], function(result) {
        if (result != undefined) {
            result.blocked ? current_list = result.blocked : current_list = [];
            result.blocked.forEach(element => {
                $('tbody').append(`<tr><td id=item>${element}</td><td><button>X</button></td></tr>`)
            });    
        }
    });

    // Asjade lisamine funtksionaalsus
    var input_box = $('#In')
    input_box.keydown(function (keyevent) {
        if (keyevent.keyCode === 13) {
            chrome.storage.sync.get(['blocked'], function (result) {
                result.blocked ? current_list = result.blocked : current_list = [];
                let inpvalue = input_box.val()
                current_list.push(inpvalue)
                chrome.storage.sync.set({blocked: current_list})

                row = (`<tr><td id=item>${inpvalue}</td><td><button>X</button></td></tr>`)
                input_box.val('')
                $('tbody').append(row)
            })
        } 
    })
    $(document).on('click', 'button', function(clicc) {
        let delete_this = $(this).parent().parent().find('#item').html()

        item_index = current_list.indexOf(delete_this)
        if (item_index != -1) {
            current_list.splice(item_index, 1)
        }     
        
        chrome.storage.sync.set({blocked: current_list})

        $(this).parent().parent().remove()

   });
}); 