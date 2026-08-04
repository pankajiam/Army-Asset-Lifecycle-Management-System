import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import InventoryIcon from "@mui/icons-material/Inventory2";
import PeopleIcon from "@mui/icons-material/People";
import AssignmentIcon from "@mui/icons-material/Assignment";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";
import HistoryIcon from "@mui/icons-material/History";
import LogoutIcon from "@mui/icons-material/Logout";

const drawerWidth = 250;

const menuItems = [
  { text: "Dashboard", icon: <DashboardIcon /> },
  { text: "Assets", icon: <InventoryIcon /> },
  { text: "Users", icon: <PeopleIcon /> },
  { text: "Assignments", icon: <AssignmentIcon /> },
  { text: "Disposal", icon: <DeleteSweepIcon /> },
  { text: "Audit Logs", icon: <HistoryIcon /> },
  { text: "Logout", icon: <LogoutIcon /> },
];

function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          backgroundColor: "#1b263b",
          color: "white",
        },
      }}
    >
      <Toolbar>
        <Box>
          <Typography variant="h6" fontWeight="bold">
            🇮🇳 AALMS
          </Typography>

          <Typography variant="body2">
            Army Asset Lifecycle
          </Typography>
        </Box>
      </Toolbar>

      <List>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.text}
            sx={{
              color: "white",
              "&:hover": {
                backgroundColor: "#415a77",
              },
            }}
          >
            <ListItemIcon sx={{ color: "white" }}>
              {item.icon}
            </ListItemIcon>

            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}

export default Sidebar;