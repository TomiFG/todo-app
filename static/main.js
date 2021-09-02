
buildList()

function buildList(){
    var container = document.getElementById('listContainer')
    var url = 'http://127.0.0.1:5000/get_items'

    container.innerHTML = ''

    fetch(url)
    .then(res => res.json())
    .then(function(data){
        console.log('Data:', data)

        var list = data.items
        for (var i in list){
            var item = `
                <div id="item-${i}" class="item">
                    <p class=item>${list[i].content}</p>
                </div> 
            `
            container.innerHTML += item
        }

    })
}


function addItem(content){
    var url = 'http://127.0.0.1:5000/add_item?content=' + content 
    
    fetch(url, {method: 'POST'})
    .then(function(response){
        buildList()
    })
}

var button = document.getElementById('inputButton')
button.onclick = function() {
    inputField = document.getElementById('inputField')
    content = inputField.value.trim()
    console.log('content:', content)

    if (content.length > 0){
        addItem(content)
    } 

    inputField.value = ''
}