
import '../App.css';
import React from 'react';

function Reg() {
  return (
      <div className="container">
          <div className="reg_block">
              <div className="name_input">
                  <h1>Username</h1>
                  <input type="text" placeholder="Enter your username"/>
              </div>
              <a href="/chat" className="sign_in_btn">
                  Sign in
              </a>
          </div>
      </div>
  );
}

export default Reg;
