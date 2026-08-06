import { useEffect, useState } from "react";

import {
    Box,
    Toolbar,
    Typography,
} from "@mui/material";

import Sidebar from "../../components/layout/Sidebar";
import Navbar from "../../components/layout/Navbar";

import UserToolbar from "../../components/users/UserToolbar";
import UserTable from "../../components/users/UserTable";
import UserDialog from "../../components/users/UserDialog";

import { getUsers } from "../../services/userService";

function Users() {

    const [users, setUsers] = useState([]);

    const [openDialog, setOpenDialog] = useState(false);

    const loadUsers = async () => {

        try {

            const data = await getUsers();

            setUsers(data);

        }

        catch (err) {

            console.log(err);

        }

    };

    useEffect(() => {

        loadUsers();

    }, []);

    const handleOpen = () => {

        setOpenDialog(true);

    };

    const handleClose = () => {

        setOpenDialog(false);

    };

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
                    User Management
                </Typography>

                <UserToolbar
                    handleOpen={handleOpen}
                />

                <UserTable
                    users={users}
                />

                <UserDialog
                    open={openDialog}
                    handleClose={handleClose}
                    loadUsers={loadUsers}
                />

            </Box>

        </Box>

    );

}

export default Users;