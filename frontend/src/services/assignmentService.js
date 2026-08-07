import axios from "../api/axios";

export const getAssignments = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/assignments/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const issueAsset = async (data) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/assignments/issue",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const returnAsset = async (data) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/assignments/return",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const transferAsset = async (data) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/assignments/transfer",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getAssetHistory = async (assetId) => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        `/assignments/history/${assetId}`,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};