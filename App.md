Sure! Here is the API documentation in English:
 
### API Documentation
 
#### Base URL
 
All API endpoints are available at the following base URL:
 
```
 
[http://localhost:5001](http://localhost:5001) 
 
```
 
#### Services
 
1. **User Service** (port 5001)
 
2. **Message Service** (port 5003)
 
3. **Feed Service** (port 5002)
 
### User Service (port 5001)
 
#### Register a User
 
**POST** `/register`
 
**Description**: Registers a new user.
 
**Request Body**:
 
```json
 
{
 
"username": "example\_user",
 
"password": "example\_password"
 
}
 
```
 
**Response**:
 
- **201 Created**:
 
```json
 
{
 
"Message": "User registered successfully"
 
}
 
```
 
- **400 Bad Request**:
 
```json
 
{
 
"Message": "User already exists"
 
}
 
```
 
#### User Login
 
**POST** `/login`
 
**Description**: Logs in a user.
 
**Request Body**:
 
```json
 
{
 
"username": "example\_user",
 
"password": "example\_password"
 
}
 
```
 
**Response**:
 
- **200 OK**:
 
```json
 
{
 
"Message": "Successfull login"
 
}
 
```
 
- **401 Unauthorized**:
 
```json
 
{
 
"Message": "User does not exist, please register"
 
}
 
```
 
or
 
```json
 
{
 
"Message": "Passwords don't match. Please try again"
 
}
 
```
 
### Message Service (port 5003)
 
#### Create a Message
 
**POST** `/message`
 
**Description**: Creates a new message from a user.
 
**Request Body**:
 
```json
 
{
 
"user\_id": 1,
 
"content": "This is a sample message"
 
}
 
```
 
**Response**:
 
- **201 Created**:
 
```json
 
{
 
"Message": "Message posted successfuly"
 
}
 
```
 
- **400 Bad Request**:
 
```json
 
{
 
"Message": "The post don't satisfy our requirements"
 
}
 
```
 
#### Delete a Message
 
**DELETE** `/message/<int:message_id>`
 
**Description**: Deletes a message by its ID.
 
**Parameters**:
 
- `message_id`: The ID of the message to delete.
 
**Response**:
 
- **200 OK**:
 
```json
 
{
 
"Message": "Message is deleted successfully"
 
}
 
```
 
- **404 Not Found**:
 
```json
 
{
 
"Message": "Message doesn't exist"
 
}
 
```
 
### Feed Service (port 5002)
 
#### Get Feed
 
**GET** `/feed`
 
**Description**: Returns the last 15 messages.
 
**Response**:
 
- **200 OK**:
 
```json
 
[
 
{
 
"User": "example\_user",
 
"Content": "This is a sample message",
 
"Date": "2023-10-01T12:00:00"
 
},
 
{
 
"User": "another\_user",
 
"Content": "Another sample message",
 
"Date": "2023-10-01T11:55:00"
 
}
 
]
 
```
 
### Conclusion
 
This documentation describes all available endpoints and their functionality for your API. Ensure that each service is running on the corresponding port, and use this documentation to interact with the API.