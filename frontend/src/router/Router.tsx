import { useContext } from 'react';
import { AuthStateContext } from '../context/AuthStateContext';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Login } from '../pages/Login';
import { Home } from '../pages/Home';
import { Register } from '../pages/Register';

export const Router = () => {
    const { isLoggedIn } = useContext(AuthStateContext);

    return <BrowserRouter>{isLoggedIn ? <ProtectedRoute /> : <PublicRoute />}</BrowserRouter>;
};

const PublicRoute = () => (
    <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
    </Routes>
);

const ProtectedRoute = () => (
    <Routes>
        <Route path="/" element={<Home />} />
    </Routes>
);
