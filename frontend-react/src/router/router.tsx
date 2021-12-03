import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { Home } from "../pages/Home";
import { Login } from "../pages/Login";
import { authState } from "../state/auth";

export const Routing = () => {
    const isAuthorized = useRecoilValue(authState);

    return (
        <BrowserRouter>
            {
                isAuthorized ?
                  <ProtectedRoute />  
                : <PublicRoute />
            }
        </BrowserRouter>
    );
}

const PublicRoute = () => <Routes>
    <Route path="/" element={<Login />} />
</Routes>

const ProtectedRoute = () => <Routes>
    <Route path="/" element={<Home />} />
</Routes>