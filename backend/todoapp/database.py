from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from todoapp import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=0)
    
    def __repr__(self):
        return f'<Item {self.id}>'