import like from '../assets/like.svg';
import like_red from '../assets/like_red.svg';
import send from '../assets/send.svg';
import '../App.css';
import React, { useState, useEffect } from 'react';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [userLikes, setUserLikes] = useState(new Set()); // Состояние для хранения лайков пользователя

    const fetchMessages = async () => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        try {
            const response = await fetch('http://127.0.0.1:5004/feed', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Получение лайков пользователя
            const likesResponse = await fetch(`http://127.0.0.1:5002/likes/user/${user_id}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (likesResponse.ok) {
                const likesData = await likesResponse.json();
                setUserLikes(new Set(likesData.liked_message_ids)); // Сохраняем лайки пользователя в виде Set для быстрого доступа
                console.log(likesData)
            }



            // Обновляем сообщения с лайками
            const updatedMessages = data.map(message => ({
                ...message,
                liked: userLikes.has(message.id), // Определяем, лайкнуто ли сообщение
            }));

            setMessages(updatedMessages);
        } catch (error) {
            console.error('Ошибка при получении сообщений:', error);
        } finally {
            setLoading(false);
        }
    };


    useEffect(() => {
        fetchMessages();
    }, []);

    const sendMessage = async () => {
        const token = localStorage.getItem('access_token');

        if (newMessage.trim() === '') {
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5003/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ content: newMessage })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            window.location.reload();
        } catch (error) {
            console.error('Ошибка при отправке сообщения:', error);
        }
    };

    const likeMessage = async (message_id) => {
        const token = localStorage.getItem('access_token');

        try {
            const response = await fetch(`http://127.0.0.1:5002/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message_id })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            setUserLikes((prev) => new Set(prev).add(message_id)); // Добавляем лайк в состояние
            // Обновляем локальное состояние сообщений
            setMessages((prevMessages) =>
                prevMessages.map(msg =>
                    msg.id === message_id ? { ...msg, liked: true, Likes: msg.Likes + 1 } : msg
                )
            );
        } catch (error) {
            console.error('Ошибка при отправке лайка:', error);
        }
    };

    const dislikeMessage = async (message_id) => {
        const token = localStorage.getItem('access_token');

        try {
            const response = await fetch(`http://127.0.0.1:5002/dislike`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message_id })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            setUserLikes((prev) => {
                const updatedLikes = new Set(prev);
                updatedLikes.delete(message_id); // Удаляем дизлайк из состояния
                return updatedLikes;
            });

            // Обновляем локальное состояние сообщений
            setMessages((prevMessages) =>
                prevMessages.map(msg =>
                    msg.id === message_id ? { ...msg, liked: false, Likes: msg.Likes - 1 } : msg
                )
            );
        } catch (error) {
            console.error('Ошибка при отправке дизлайка:', error);
        }
    };

    const handleLikeClick = async (id) => {
        if (userLikes.has(id)) {
            // Если сообщение уже лайкнуто, отправляем дизлайк
            await dislikeMessage(id);
        } else {
            // Иначе отправляем лайк
            await likeMessage(id);
        }
    };

    return (
        <div className="chat_block">
            {loading ? (
                <div>Loading messages...</div>
            ) : (
                <div className="messages_block">
                    {messages.map((message) => (
                        <div className="message" key={message.id}>
                            <div className="usr_name">
                                <h1>{message.User}</h1>
                            </div>
                            <div className="msg_text">
                                <h2>{message.Content}</h2>
                            </div>
                            <div className="like" onClick={() => handleLikeClick(message.id)} style={{ cursor: 'pointer' }}>
                                <img src={message.liked ? like_red : like} alt="Like" />
                                <span id="num_of_likes">{message.Likes}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
            <div className="down_panel">
                <textarea
                    placeholder="Your message"
                    maxLength={400}
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                />
                <button className="enter" onClick={sendMessage}>
                    <img src={send} alt="Send" />
                </button>
            </div>
            <a href="/chat" className="sign_in_btn unvisib">
                Sign in
            </a>
        </div>
    );
}

export default Chat;
