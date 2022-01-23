
function runCartFilter (htmlentity) {
    let out_array = []
    if (htmlentity.length > 0) {
        for (i=0; i<htmlentity.length; i++) {
            out_array.push(htmlentity[i].href)
        }
        chrome.storage.sync.get(['blocked'], function (blocked) {
            $.post({
                url: 'http://127.0.0.1:5000/',
                data: JSON.stringify({
                    'urls': out_array,
                    'forbidden': blocked.blocked
                }, null, '\t'),
                contentType: 'application/json',
                success: function(result) {
                    for ([key, value] of Object.entries(result)) {
                        if (htmlentity[key] != undefined) {
                            let classes = htmlentity[key].parentNode.classList

                            if (value.length > 0) {
                                classes.add("extension-blocked")
                            }
                            else if (value.length == 0) {
                                classes.remove("extension-blocked")
                            }
                        }
                    }
                }
            })
        })
    }
}

chrome.storage.sync.onChanged.addListener(function () {cartWrapper()})

chrome.runtime.onMessage.addListener(
    function(request) {
        console.log(request)
        if (request.page == 'cart') {
            cartWrapper()
        }
    }
);

a = []
  

function cartWrapper (nm) {
    var func = setInterval(
        function () {
            a.push(func);
            console.log(nm);
            len = document.getElementsByClassName('Product__image-wrapper');
            if (len.length > 0) {
                runCartFilter(len);
                clearInterval(func);
            }
        },
        100
    )
}
