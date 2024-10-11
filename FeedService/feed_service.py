from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/softarch5'
app.config['JWT_SECRET_KEY'] = "717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61"
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.DEBUG)


@app.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    try:
        current_user_id = get_jwt_identity()

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "Message": "Authorization token is missing or invalid"
            }), 401

        token = auth_header.split(' ')[1]

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get('http://localhost:5003/messages', headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to fetch messages from message_service: {response.status_code} {response.text}")
            return jsonify({
                "Message": "Failed to fetch messages from message_service"
            }), 500

        messages = response.json()
        feed = []

        response = requests.get(f'http://localhost:5002/likes/user/{current_user_id}')
        if response.status_code != 200:
            logging.error(f"Failed to fetch user likes from like_service: {response.status_code} {response.text}")
            return jsonify({
                "Message": "Failed to fetch user likes from like_service"
            }), 500

        user_likes = response.json().get('liked_message_ids', [])

        for msg in messages:
            response = requests.get(f'http://localhost:5002/likes/{msg["id"]}')
            if response.status_code != 200:
                logging.error(f"Failed to fetch likes for message from like_service: {response.status_code} {response.text}")
                return jsonify({
                    "Message": "Failed to fetch likes for message from like_service"
                }), 500

            likes = response.json().get('likes', 0)

            feed.append({
                'id': msg['id'],
                'User': msg['username'],
                'Content': msg['content'],
                'Date': msg['date'],
                'Likes': likes,
                'LikedByCurrentUser': msg['id'] in user_likes
            })
        print("The work is done")
        return jsonify(feed), 200
    except Exception as e:
        logging.error(f"Error during feed retrieval: {e}")
        return jsonify({
            "Message": "Internal Server Error"
        }), 500


@app.route('/like', methods=['POST'])
@jwt_required()
def like():
    try:
        data = request.json
        message_id = data.get('message_id')

        if not message_id:
            return jsonify({
                "Message": "Message ID is required"
            }), 400

        response = requests.post(f'http://localhost:5002/like', json={'message_id': message_id})
        if response.status_code != 201:
            logging.error(f"Failed to add like: {response.status_code} {response.text}")
            return jsonify({
                "Message": "Failed to add like"
            }), 500

        return jsonify({
            "Message": "Like added successfully"
        }), 201
    except Exception as e:
        logging.error(f"Error during like addition: {e}")
        return jsonify({
            "Message": "Internal Server Error"
        }), 500


@app.route('/unlike', methods=['POST'])
@jwt_required()
def unlike():
    try:
        data = request.json
        message_id = data.get('message_id')

        if not message_id:
            return jsonify({
                "Message": "Message ID is required"
            }), 400

        response = requests.post(f'http://localhost:5002/dislike', json={'message_id': message_id})
        if response.status_code != 200:
            logging.error(f"Failed to remove like: {response.status_code} {response.text}")
            return jsonify({
                "Message": "Failed to remove like"
            }), 500

        return jsonify({
            "Message": "Like removed successfully"
        }), 200
    except Exception as e:
        logging.error(f"Error during like removal: {e}")
        return jsonify({
            "Message": "Internal Server Error"
        }), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0', port=5004, debug=True)