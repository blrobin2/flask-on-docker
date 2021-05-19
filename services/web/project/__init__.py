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


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload New File</title>
    </head>
    <body>
        <form action="" method="post" enctype="multipart/form-data">
            <p>
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </p>
        </form>
    </body>
    </html>
    """
