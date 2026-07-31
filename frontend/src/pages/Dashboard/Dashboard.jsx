import { Typography, Box } from "@mui/material";

function Dashboard() {
    return (
        <Box sx={{ p: 4 }}>
            <Typography variant="h3">
                🎉 Login Successful
            </Typography>

            <Typography variant="h5" sx={{ mt: 2 }}>
                Army Asset Lifecycle Management Dashboard
            </Typography>
        </Box>
    );
}

export default Dashboard;