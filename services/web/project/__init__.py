from datetime import datetime
from flask import Flask, jsonify, request
from flask.helpers import send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

CORS(app, resources={r'/*': {'origins': '*'}})


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    from_email = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(255), nullable=False, default='(No Subject)')
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    archived = db.Column(db.Boolean(), nullable=False, default=False)
    read = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, from_email, subject, body, sent_at=None):
        self.from_email = from_email
        self.subject = subject
        self.body = body
        if sent_at is not None:
            self.sent_at = sent_at


@app.route("/api")
def index():
    return jsonify(hello="world")
