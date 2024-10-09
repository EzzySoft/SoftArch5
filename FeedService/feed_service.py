from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kmmrwsgr:UMg6sKjYUG3nhI6D3fTjSU3vMpjGjYCI@abul.db.elephantsql.com/kmmrwsgr'
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    user = db.relationship('User', backref='messages')
    likes = db.Column(db.Integer, default=0)


@app.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    current_user_id = get_jwt_identity()
    messages = Message.query.order_by(Message.id.desc()).limit(10).all()
    feed = []

    response = requests.get(f'http://localhost:5002/likes/user/{current_user_id}')
    user_likes = response.json().get('liked_message_ids', [])

    for msg in messages:
        response = requests.get(f'http://localhost:5002/likes/{msg.id}')
        likes = response.json().get('likes', 0)

        feed.append({
            'id': msg.id,
            'User': msg.user.username,
            'Content': msg.content,
            'Date': msg.date,
            'Likes': likes,
            'LikedByCurrentUser': msg.id in user_likes
        })

    return jsonify(feed), 200


@app.route('/like', methods=['POST'])
@jwt_required()
def like():
    data = request.json
    message_id = data.get('message_id')

    if not message_id:
        return jsonify({
            "Message": "Message ID is required"
        }), 400

    message = Message.query.get(message_id)
    if not message:
        return jsonify({
            "Message": "Message not found"
        }), 404

    message.likes += 1
    db.session.commit()

    return jsonify({
        "Message": "Like added successfully"
    }), 201


@app.route('/unlike', methods=['POST'])
@jwt_required()
def unlike():
    data = request.json
    message_id = data.get('message_id')

    if not message_id:
        return jsonify({
            "Message": "Message ID is required"
        }), 400

    message = Message.query.get(message_id)
    if not message:
        return jsonify({
            "Message": "Message not found"
        }), 404

    if message.likes > 0:
        message.likes -= 1
        db.session.commit()

    return jsonify({
        "Message": "Like removed successfully"
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5004)