from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from todoapp import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class DbObject:

    class Item(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String(150), nullable=False)
        completed = db.Column(db.Boolean, default=0)
        
        def __repr__(self):
            return f'<Item {self.id}>'


    def query_items(self): 
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
        return response

    def add_item(self, content):
        new_item = Item(content=content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return True
        except:
            return False

    def  delete_item(self, id): 
        item_to_delete = Item.query.get_or_404(id) 

        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            return True
        except:
            return False

    def update_item(self, id, new_content):
        item_to_update = Item.query.get_or_404(id)
        
        item_to_update.content = new_content 

        try:
            db.session.commit()
            return True
        except:
            return False


    def change_state(self, id, new_state):
        item_to_update = Item.query.get_or_404(id)

        item_to_update.completed = int(new_state)

        try:
            db.session.commit()
            return True
        except:
            return False