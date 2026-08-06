import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Assets from "../pages/assets/Assets";
import Users from "../pages/users/Users";

function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/assets" element={<Assets />} />
                <Route path="/users" element={<Users />} />
            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;