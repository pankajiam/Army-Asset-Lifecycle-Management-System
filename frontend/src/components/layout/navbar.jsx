import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Avatar,
} from "@mui/material";

function Navbar() {
  return (
    <AppBar
      position="fixed"
      sx={{
        width: "calc(100% - 250px)",
        ml: "250px",
        backgroundColor: "#ffffff",
        color: "#000",
        boxShadow: 2,
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <Typography variant="h6" fontWeight="bold">
          Army Asset Lifecycle Management System
        </Typography>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2,
          }}
        >
          <Typography>
            Welcome, Admin
          </Typography>

          <Avatar sx={{ bgcolor: "#1976d2" }}>
            A
          </Avatar>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;