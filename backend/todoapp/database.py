from flask_sqlalchemy import SQLAlchemy
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

    @classmethod
    def query_items(cls, itm=Item): 
        items_list = itm.query.all()

        items = []    

        for item in items_list:
            item_data = {}
            item_data['id'] = item.id
            item_data['content'] = item.content
            item_data['completed'] = item.completed
            items.append(item_data)
        
        response = {
            "total": len(items_list),
            "items": items
        }
        return response

    @classmethod
    def add_item(cls, content, itm=Item):
        new_item = itm(content=content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def  delete_item(cls, id, itm=Item): 
        item_to_delete = itm.query.get_or_404(id) 

        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def update_item(cls, id, new_content, itm=Item):
        item_to_update = itm.query.get_or_404(id)
        
        item_to_update.content = new_content 

        try:
            db.session.commit()
            return True
        except:
            return False


    @classmethod
    def change_state(cls, id, new_state, itm=Item):
        item_to_update = itm.query.get_or_404(id)

        item_to_update.completed = int(new_state)

        try:
            db.session.commit()
            return True
        except:
            return False