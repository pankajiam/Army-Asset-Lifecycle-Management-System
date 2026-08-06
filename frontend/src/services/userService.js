import axios from "../api/axios";

export const getUsers = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/users/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const createUser = async (user) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/users/",
        user,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getRoles = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/roles/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getRanks = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/ranks/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getUnits = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/units/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};