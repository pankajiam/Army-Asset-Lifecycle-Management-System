import axios from "../api/axios";

export const getAuditLogs = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/audit/",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;
};