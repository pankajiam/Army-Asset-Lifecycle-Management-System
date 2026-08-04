import axios from "../api/axios";

export const getDashboardData = async () => {

    const token = localStorage.getItem("token");

    const response = await axios.get(
        "/dashboard/summary",
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    return response.data;
};