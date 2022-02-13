
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

function cartWrapper () {
    var func = setInterval(
        function () {
            len = document.getElementsByClassName('Product__image-wrapper');
            if (len.length > 0) {
                runCartFilter(len);
                clearInterval(func);
            }
        },
        100
    )
}


function runProductFilter ( ) {
    //get koostis
    let koostisosad = $(".AttributeAccordion:contains('Koostis')");
    if (koostisosad.length > 0) {
        var koostised_allergeenid = koostisosad.find('.Accordion__content').html().toLowerCase();
        if (koostised_allergeenid.search('(toode)+( )*(võib)') != -1 || koostised_allergeenid.search('(võib)+( )*(sisaldada)') != -1) {
            koostised_allergeenid = koostised_allergeenid.split('võib')[0];
        }    
    }

    let allergeenid = $(".AttributeAccordion:contains('Allergeenid')")
    if (allergeenid.length > 0) {
        allergeenid = allergeenid.find('.Accordion__content').html().toLowerCase();
        if (allergeenid.search('(toode)+( )*(võib)') != -1 || allergeenid.search('(võib)+( )*(sisaldada)') != -1) {
            koostised_allergeenid += allergeenid.split('võib')[0];
        }
        else {
            koostised_allergeenid += allergeenid
        }
    }
    
    //filter against unwished ingrs.
    chrome.storage.sync.get(['blocked'], function(result) {
        var blocked_ingredients = []
        result.blocked.forEach(element => {
            if (koostised_allergeenid.includes(element)) {
                blocked_ingredients.push(element)
            }
        })
        if (blocked_ingredients.length > 0) {
            alert('Sisaldab järgmiseid: ' + blocked_ingredients.join(', '))
        }
    })
}


function productWrapper ( ) {
    let func = setInterval(
        function() {
            len = document.getElementsByClassName('AttributeAccordion__content')
            if (len.length > 0) {
                runProductFilter()
                clearInterval(func)
            }
        },
        100
    )
}

chrome.storage.sync.onChanged.addListener(function () {cartWrapper()})

chrome.runtime.onMessage.addListener(
    function(request) {
        if (request.page == 'cart') {
            cartWrapper()
        }
        if (request.page == 'product') {
            productWrapper()
        }
    }
);

a = []