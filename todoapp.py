from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
CORS(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Item {self.id}>'

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html')

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

@app.route('/get_item/<id>')
def getItem(id):
    item = Item.query.get_or_404(id)
    
    if not item:
        return make_response(jsonify('item not found'), 404)
    
    item_dict = {}
    item_dict['id'] = id
    item_dict['content'] = item.content
    item_dict['completed'] = item.completed

    return make_response(jsonify(item_dict), 200)


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


@app.route('/change_state/<id>', methods=['PUT'])
def changeState(id):
    item_to_update = Item.query.get_or_404(id)
    data = request.get_json()
    new_state = data.get('completed', False)    

    item_to_update.completed = new_state

    try:
        db.session.commit()
        return make_response(jsonify('Item status updated'), 200)
    except:
        return make_response(jsonify('There was an issue updating the item state'), 500)

if __name__ == '__main__':
    app.run(debug=True)