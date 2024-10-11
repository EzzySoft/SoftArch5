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

#### Шаг 1: Create docker network


```bash
docker network create my_network
```

#### Шаг 2: Create image for database

Если у вас есть Dockerfile для базы данных, создайте образ:

```bash
docker build -t my_postgres -f ./Database/Dockerfile ./Database
```

#### Шаг 3: Run database

```bash
docker run -d \
  --name postgres_db \
  --network my_network \
  -p 5432:5432 \
  -e POSTGRES_DB=softarch5 \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -v postgres_data:/var/lib/postgresql/data \
  my_postgres
```

#### Шаг 4: Create images for services


```bash
docker build -t user_service -f ./UserService/Dockerfile ./UserService
```
Repeat for every service

#### Шаг 5: Run services


```bash
docker run -d \
  --name user_service \
  --network my_network \
  -p 5001:5001 \
  -e SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@postgres_db:5432/softarch5 \
  -e JWT_SECRET_KEY=717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61 \
  user_service
```

Repeat this step for every service (`message_service`, `like_service`, `feed_service`).


#### Create image for database

```bash
docker build -t my_postgres -f ./Database/Dockerfile ./Database
```

#### Run the database

```bash
docker run -d \
  --name postgres_db \
  --network my_network \
  -p 5432:5432 \
  -e POSTGRES_DB=softarch5 \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -v postgres_data:/var/lib/postgresql/data \
  my_postgres
```

#### Create images for services

```bash
docker build -t user_service -f ./UserService/Dockerfile ./UserService
docker build -t message_service -f ./MessageService/Dockerfile ./MessageService
docker build -t like_service -f ./LikeService/Dockerfile ./LikeService
docker build -t feed_service -f ./FeedService/Dockerfile ./FeedService
```

#### Run services

```bash
docker run -d \
  --name user_service \
  --network my_network \
  -p 5001:5001 \
  -e SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@postgres_db:5432/softarch5 \
  -e JWT_SECRET_KEY=717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61 \
  user_service

docker run -d \
  --name message_service \
  --network my_network \
  -p 5003:5003 \
  -e SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@postgres_db:5432/softarch5 \
  -e JWT_SECRET_KEY=717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61 \
  message_service

docker run -d \
  --name like_service \
  --network my_network \
  -p 5002:5002 \
  -e SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@postgres_db:5432/softarch5 \
  -e JWT_SECRET_KEY=717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61 \
  like_service

docker run -d \
  --name feed_service \
  --network my_network \
  -p 5004:5004 \
  -e SQLALCHEMY_DATABASE_URI=postgresql://myuser:mypassword@postgres_db:5432/softarch5 \
  -e JWT_SECRET_KEY=717ac506950da0ccb6404cdd5e7591f72018a20cbca27c8a423e9c9e5626ac61 \
  feed_service
```
 
### Conclusion
 
This documentation describes all available endpoints and their functionality for your API. Ensure that each service is running on the corresponding port, and use this documentation to interact with the API.