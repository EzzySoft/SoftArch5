from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kmmrwsgr:UMg6sKjYUG3nhI6D3fTjSU3vMpjGjYCI@abul.db.elephantsql.com/kmmrwsgr'
db = SQLAlchemy(app)
jwt = JWTManager(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@app.route('/message', methods=['POST'])
@jwt_required()
def post_message():
    data = request.json
    user_id = get_jwt_identity()
    content = data.get('content')

    if not content or len(content) > 400:
        return jsonify({
            "Message": "The post doesn't satisfy our requirements",
        }), 400

    mes = Message(user_id=user_id, content=content)
    db.session.add(mes)
    db.session.commit()
    return jsonify({
        "Message": "Message posted successfully",
    }), 201


@app.route('/message/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message is None:
        return jsonify({
            "Message": "Message doesn't exist"
        }), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({
        "Message": "Message is deleted successfully"
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5003)