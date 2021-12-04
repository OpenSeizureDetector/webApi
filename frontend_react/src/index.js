import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import Login from './Login';
import Logout from './Logout';
import Profile from './Profile';
import PwReset from './PwReset';
import Register from './Register';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
	<BrowserRouter>
	<Routes>
	<Route path = "/" element={<App />} />
	<Route path = "/login" element={<Login />} />
	<Route path = "/profile" element={<Profile />} />
	<Route path = "/reset-pw" element={<PwReset />} />
	<Route path = "/logout" element={<Logout />} />
	<Route path = "/register" element={<Register />} />
	</Routes>
	</BrowserRouter>
	</React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
