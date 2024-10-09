import like from '../assets/like.svg';
import like_red from '../assets/like_red.svg';
import send from '../assets/send.svg';
import '../App.css';
import React, { useState } from 'react';

function Chat() {
    const [messages, setMessages] = useState([
        { id: 1, text: 'Mozzarella stuffed string spinach lovers onions garlic party', likesCount: 1518, liked: false },
        { id: 2, text: 'Cheese Chicago pineapple parmesan steak party crust', likesCount: 897, liked: false },
        { id: 3, text: 'Mozzarella stuffed string spinach lovers onions garlic party burnt. Broccoli chicken beef banana mozzarella. Cheese Chicago pineapple parmesan steak party crust. String deep Philly spinach banana. Garlic meatball olives and mozzarella pesto. Tossed white olives green pesto mozzarella cheese bbq parmesan marinara. Buffalo pesto tossed garlic Hawaiian meat. large bell platter fresh bacon anchovies', likesCount: 107, liked: false },

    ]); // Инициализируем массив с сообщениями

    const handleLikeClick = (id) => {
        setMessages(messages.map(msg =>
            msg.id === id
                ? { ...msg, liked: !msg.liked, likesCount: msg.liked ? msg.likesCount - 1 : msg.likesCount + 1 }
                : msg
        )); // Обновляем только конкретное сообщение
    };

    return (
        <div className="chat_block">
            <div className="messages_block">
                {messages.map((message) => (
                    <div className="message" key={message.id}>
                        <div className="usr_name">
                            <h1>Anton Fadeenkov</h1>
                        </div>
                        <div className="msg_text">
                            <h2>{message.text}</h2>
                        </div>
                        <div className="like" onClick={() => handleLikeClick(message.id)} style={{ cursor: 'pointer' }}>
                            <img src={message.liked ? like_red : like} alt="Like" />
                            <span id="num_of_likes">{message.likesCount}</span>
                        </div>
                    </div>
                ))}
            </div>
            <div className="down_panel unvisib" >
                <textarea placeholder="Your message" maxLength={400}></textarea>
                <button className="enter">
                    <img src={send} alt="Send" />
                </button>
            </div>
            <a href="/chat" className="sign_in_btn">
                Sign in
            </a>
        </div>
    );
}

export default Chat;