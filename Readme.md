# NotTwitter

## Description
A microservices-based application that has a registration by username and allow to post short messages, read others messages and like them.

## Features
- User can register using username.
- Users can send messages when logged in, with a maximum of 400 characters.
- User can read a feed of the latest 10 messages.
- User can react on message.
- Separate services for users, messages, and likes.

## Usage
Start the services:
* User Service:
    python user_service.py
* Message Service:
    python message_service.py
* Like Service:
    python like_service.py
* Feed Service:
    python feed_service.py
### The code launch is registered in App.md
## Notes
* Make your PostgreSQL database running and with all set up configs. 
* Also JWT secret key should be in saved in secure manner