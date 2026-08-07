import axios from "../api/axios";


export const requestDisposal = async (data) => {

    const token = localStorage.getItem("token");

    const response = await axios.post(
        "/disposals/request",
        data,
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};


export const approveDisposal = async (disposalId) => {

    const token = localStorage.getItem("token");

    const response = await axios.put(
        `/disposals/approve/${disposalId}`,
        {},
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};

export const getPendingDisposals = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/disposals/pending",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;

};