
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chat from './pages/Chat';
import Reg from './pages/Reg';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/chat" element={<Chat />} />
                <Route path="/" element={<Reg />} />
            </Routes>
        </Router>
    );
}

export default App;