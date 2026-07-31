import api from "../api/axios";

export const login = async (army_number, password) => {

    const response = await api.post("/users/login", {
        army_number,
        password,
    });

    return response.data;
};