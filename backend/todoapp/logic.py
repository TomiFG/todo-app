from flask import request, jsonify, make_response
from todoapp import app
from todoapp.database import Item, db

@app.route('/get_items')
def getItems():
    items_list = Item.query.all()

    items = []    

    for item in items_list:
        item_data = {}
        item_data['id'] = item.id
        item_data['content'] = item.content
        item_data['completed'] = item.completed
        items.append(item_data)
    
    response = jsonify(
        {
            "total": len(items_list),
            "items": items
        }
    )

    return make_response(response, 200) 


@app.route('/add_item', methods=['POST'])
def addItem():
    item_content = request.args.get('content')
    new_item = Item(content=item_content)

    try:
        db.session.add(new_item)
        db.session.commit()
        return make_response(jsonify('New item created.'), 201)
    except:
        return make_response(jsonify('There was an issue creating the new item.'), 500)


@app.route('/delete_item/<id>', methods=['DELETE'])
def deleteItem(id):
    item_to_delete = Item.query.get_or_404(id) 

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return make_response(jsonify('Item deleted.'), 200)
    except:
        return make_response(jsonify('There was an issue deleting the item.'), 500)


@app.route('/update_item/<id>', methods=['PUT'])
def updateItem(id):
    item_to_update = Item.query.get_or_404(id)
    new_content = request.args.get('content')
    
    item_to_update.content = new_content 

    try:
        db.session.commit()
        return make_response(jsonify('Item updated.'), 200)
    except:
        return make_response(jsonify('There was an issue updating the item.'), 500)


@app.route('/change_state/<id>/<state>', methods=['PUT'])
def changeState(id, state):
    item_to_update = Item.query.get_or_404(id)
    new_state = int(state) 

    item_to_update.completed = new_state

    try:
        db.session.commit()
        return make_response(jsonify('Item status updated'), 200)
    except:
        return make_response(jsonify('There was an issue updating the item state'), 500)