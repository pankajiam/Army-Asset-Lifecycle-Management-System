import axios from "../api/axios";

export const getAssets = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/assets/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const createAsset = async (asset) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/assets/",
        asset,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const updateAsset = async (assetId, asset) => {

    const token = localStorage.getItem("token");

    const response = await axios.put(
        `/assets/${assetId}`,
        asset,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getAssetCategories = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/asset-categories/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getAssetStatuses = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/asset-status/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};