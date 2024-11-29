from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@mysql:3306/message_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Message field is required"}), 400

        message = Message(content=data['message'])
        db.session.add(message)
        db.session.commit()
        return jsonify({"message": "Message stored successfully!"})

    # GET: Retrieve all messages
    messages = Message.query.all()
    return jsonify([{"id": msg.id, "content": msg.content} for msg in messages])
