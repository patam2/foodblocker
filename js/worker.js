var out_array = [];

function runCartFilter (htmlentity) {
    console.log('Here')
    if (htmlentity.length > 0) {
        for (i=0; i<htmlentity.length; i++) {
            out_array.push(htmlentity[i].href)
        }
        console.log(out_array)
        $.post({
            url: 'http://127.0.0.1:5000/',
            data: JSON.stringify({
                'urls': out_array,
                'forbidden': ['sinep']
            }, null, '\t'),
            contentType: 'application/json',
            success: function(result) {
                for (const [key, value] of Object.entries(result)) {
                    if (value.length > 0 && htmlentity[key] != undefined) {
                        htmlentity[key].classList.add("extension-blocked")
                    }
                }
            }
        })
        out_array = []
    }
}

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
    var func = setInterval(  //lol ma otsisin miks see loopib 24/7 ja see oli selle parast et mai pannud var
        function () {
            a.push(func)
            console.log(nm)
            len = document.getElementsByClassName('Product__image-wrapper')
            if (len.length > 0) {
                runCartFilter(len)
                clearInterval(func)
                return
            }
        },
        100
    )
}
