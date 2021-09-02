
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
            id = list[i].id
            var item = `
                <div id="item-${id}" class="item">
                    <input type="checkbox" id="check-${id}" onchange="changeState(${id})" >
                    <p id="p-${id}" class="iText">${list[i].content}</p>
                    <button class="edButton" onclick="editItem(${id})">edit</button>
                    <button class="delButton" onclick="deleteItem(${id})">x</button>
                </div> 
            `
            container.innerHTML += item

        }
       
        for (var i in list){
            document.getElementById('check-' + list[i].id).checked = list[i].completed
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

// calls the api to change the (completion) state of an item
function changeState(id){
    var state_tf = document.getElementById('check-' + id).checked
    if (state_tf){ state = 1 }else{ state = 0 }

    var url = 'http://127.0.0.1:5000/change_state/' + id + '/' + state
    
    fetch(url, {method: 'PUT'})
}

// calls the api to updated an item's content
function updateItem(id){
    var content = document.getElementById('editField-' + id).value.trim()
    var url = 'http://127.0.0.1:5000/update_item/' + id + '?content=' + content

    mainInput = document.getElementById('mainInput')
    mainInput.style.display = 'block'

    fetch(url, {method: 'PUT'})
    .then(function(response){
        buildList()
    })
}

// provides an interface for editing an item
function editItem(id){
    var container = document.getElementById('listContainer')
    var current_content = document.getElementById('p-' + id).innerText
    console.log(current_content)

    var edit_div = `
        <div id="edit-${id}" class="item">
            <input id="editField-${id}" type="text" class="inputField" value="${current_content}">
            <button class="saveBtn" onclick="updateItem(${id})">save</button>
        </div> 
    `
    container.innerHTML = edit_div

    mainInput = document.getElementById('mainInput')
    mainInput.style.display = 'none'
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

