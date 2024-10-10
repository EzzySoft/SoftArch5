import React, { useState } from 'react';
import '../App.css';

function Reg() {
    const [username, setUsername] = useState('');

    const handleSignIn = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5001/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username })
            });

            const data = await response.json();

            if (data.Message === 'User already exists') {
                await loginUser();
            }

            if (data.Message === 'User registered successfully') {
                await loginUser();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const loginUser = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5001/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username })
            });

            const loginData = await response.json();

            if (loginData.access_token) {
                localStorage.setItem('access_token', loginData.access_token);
                localStorage.setItem('user_id', loginData.user_id);
                console.log('User logged in, token saved:', loginData.access_token);
                window.location.href = '/chat';
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    };

    return (
        <div className="container">
            <div className="reg_block">
                <div className="name_input">
                    <h1>Username</h1>
                    <input
                        type="text"
                        placeholder="Enter your username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <button className="sign_in_btn" onClick={handleSignIn}>
                    Sign in
                </button>
            </div>
        </div>
    );
}

export default Reg;
