out_array = []

func = setInterval( 
    function () {
        len = document.getElementsByClassName('Product__image-wrapper')
        if (len.length > 0) {
            console.log(
                'Here'
            )
            for (i=0; i<len.length; i++) {
                out_array.push(len[i].href)
            }
            $.post({
                url: 'http://127.0.0.1:5000/',
                data: JSON.stringify({
                    'urls': out_array,
                    'forbidden': ['sinep']
                }, null, '\t'),
                contentType: 'application/json',
                success: function(result) {
                    for (const [key, value] of Object.entries(result)) {
                        if (value.length > 0) {
                            len[key].classList.add("extension-blocked")
                        }
                    }
                }
            })
            clearInterval(func)
        }
    },
    100
)