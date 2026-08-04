import { useEffect, useState } from "react";

import { Box, Toolbar, Typography, Grid } from "@mui/material";

import Inventory2Icon from "@mui/icons-material/Inventory2";
import PeopleIcon from "@mui/icons-material/People";
import AssignmentIcon from "@mui/icons-material/Assignment";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";

import Sidebar from "../../components/layout/Sidebar";
import Navbar from "../../components/layout/Navbar";
import StatCard from "../../components/dashboard/StatCard";

import { getDashboardData } from "../../services/dashboardService";

function Dashboard() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        async function loadDashboard() {

            try {

                const data = await getDashboardData();

                console.log("Dashboard Data:", data);

                setStats(data);

            } catch (err) {

                console.log(err);

            }

        }

        loadDashboard();

    }, []);

    return (
        <Box sx={{ display: "flex" }}>

            <Sidebar />

            <Navbar />

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                }}
            >
                <Toolbar />

                <Typography
                    variant="h4"
                    fontWeight="bold"
                    gutterBottom
                >
                    Dashboard
                </Typography>

                <Grid container spacing={3} sx={{ mt: 1 }}>

                    <Grid item xs={12} md={6} lg={3}>
                        <StatCard
                            title="Total Assets"
                            value={stats?.total_assets ?? 0}
                            color="#1976d2"
                            icon={<Inventory2Icon fontSize="large" />}
                        />
                    </Grid>

                    <Grid item xs={12} md={6} lg={3}>
                        <StatCard
                            title="Assigned Assets"
                            value={stats?.assigned_assets ?? 0}
                            color="#2e7d32"
                            icon={<PeopleIcon fontSize="large" />}
                        />
                    </Grid>

                    <Grid item xs={12} md={6} lg={3}>
                        <StatCard
                            title="Available Assets"
                            value={stats?.available_assets ?? 0}
                            color="#ed6c02"
                            icon={<AssignmentIcon fontSize="large" />}
                        />
                    </Grid>

                    <Grid item xs={12} md={6} lg={3}>
                        <StatCard
                            title="Pending Disposals"
                            value={stats?.pending_disposals ?? 0}
                            color="#d32f2f"
                            icon={<WarningAmberIcon fontSize="large" />}
                        />
                    </Grid>

                </Grid>

            </Box>

        </Box>
    );
}

export default Dashboard;