
buildList()

// calls the api to get all the items and builds the list
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
                <div class="item">
                    <p class="iText">${list[i].content}</p>
                    <button class="delButton" >edit</button>
                    <button class="delButton" onclick="deleteItem(${list[i].id})">-</button>
                </div> 
            `
            container.innerHTML += item
        }

    })
}

// calls the api to add a new item and re-build the list
function addItem(content){
    var url = 'http://127.0.0.1:5000/add_item?content=' + content 
    
    fetch(url, {method: 'POST'})
    .then(function(response){
        buildList()
    })
}

// calls the api to delete an item and re-build the list
function deleteItem(id){
    var url = 'http://127.0.0.1:5000/delete_item/' + id 

    fetch(url, {method: 'DELETE'})
    .then(function(response){
        buildList()
    })
}

//run addItem only if there's something other than whitespace to submit
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

