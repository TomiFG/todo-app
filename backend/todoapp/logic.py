from flask import jsonify, make_response, request
from todoapp import app
from todoapp.database import DbObject as db


@app.route('/get_items')
def getItems():
    result = jsonify(db.query_items())
    return make_response(result, 200) 


@app.route('/add_item', methods=['POST'])
def addItem():
    item_content = request.args.get('content')
    success = db.add_item(item_content)

    if success:
        return make_response(jsonify('New item created.'), 201)
    else:
        return make_response(jsonify('There was an issue creating the new item.'), 500)


@app.route('/delete_item/<id>', methods=['DELETE'])
def deleteItem(id):
    success = db.delete_item(id)

    if success:
        return make_response(jsonify('Item deleted.'), 200)
    else:
        return make_response(jsonify('There was an issue deleting the item.'), 500)


@app.route('/update_item/<id>', methods=['PUT'])
def updateItem(id):
    new_content = request.args.get('content')
    success = db.update_item(id, new_content)

    if success:
        return make_response(jsonify('Item updated.'), 200)
    else:
        return make_response(jsonify('There was an issue updating the item.'), 500)


@app.route('/change_state/<id>/<state>', methods=['PUT'])
def changeState(id, state):
    new_state = int(state) 
    success = db.change_state(id, new_state)

    if success:
        return make_response(jsonify('Item status updated'), 200)
    else:
        return make_response(jsonify('There was an issue updating the item state'), 500)
