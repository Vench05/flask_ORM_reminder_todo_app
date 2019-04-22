import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = '\x1a\x1f\xc5Z\x15>\x81\x8fQ\xac\xea\xeb\xdb\x19\x8b`\xc3\x88\x92\xed\xc1s\x93\xeb'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vench@localhost:5432/reminder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
