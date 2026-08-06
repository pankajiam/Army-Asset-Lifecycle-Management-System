import { useState, useEffect } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    Grid,
    MenuItem,
} from "@mui/material";

import {
    createUser,
    getRoles,
    getRanks,
    getUnits,
} from "../../services/userService";

function UserDialog({ open, handleClose, loadUsers }) {

    const [user, setUser] = useState({
        army_number: "",
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        role_id: "",
        rank_id: "",
        unit_id: "",
    });

    const [roles, setRoles] = useState([]);

    const [ranks, setRanks] = useState([]);

    const [units, setUnits] = useState([]);

    useEffect(() => {

        loadMasters();

    }, []);

    const loadMasters = async () => {

        try {

            const roleData = await getRoles();

            const rankData = await getRanks();

            const unitData = await getUnits();

            setRoles(roleData);

            setRanks(rankData);

            setUnits(unitData);

        }

        catch (err) {

            console.log(err);

        }

    };

    const handleChange = (e) => {

        setUser({
            ...user,
            [e.target.name]: e.target.value,
        });

    };

    const resetForm = () => {

        setUser({
            army_number: "",
            first_name: "",
            last_name: "",
            email: "",
            phone: "",
            password: "",
            role_id: "",
            rank_id: "",
            unit_id: "",
        });

    };

    const handleSubmit = async () => {

        try {

            const payload = {
                ...user,
                role_id: Number(user.role_id),
                rank_id: Number(user.rank_id),
                unit_id: Number(user.unit_id),
            };

            await createUser(payload);

            alert("User Created Successfully");

            await loadUsers();

            resetForm();

            handleClose();

        }
        catch (err) {

            console.log(err);

            if (err.response) {

                alert(JSON.stringify(err.response.data));

            }
            else {

                alert(err.message);

            }

        }

    };

    return (

        <Dialog
            open={open}
            onClose={handleClose}
            maxWidth="md"
            fullWidth
        >

            <DialogTitle>
                Add User
            </DialogTitle>

            <DialogContent>

                <Grid container spacing={2} sx={{ mt: 1 }}>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Army Number"
                            name="army_number"
                            value={user.army_number}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="First Name"
                            name="first_name"
                            value={user.first_name}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Last Name"
                            name="last_name"
                            value={user.last_name}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Email"
                            name="email"
                            value={user.email}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Phone"
                            name="phone"
                            value={user.phone}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            type="password"
                            label="Password"
                            name="password"
                            value={user.password}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            select
                            label="Role"
                            name="role_id"
                            value={user.role_id}
                            onChange={handleChange}
                        >
                            {roles.map((role) => (
                                <MenuItem
                                    key={role.role_id}
                                    value={role.role_id}
                                >
                                    {role.role_name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            select
                            label="Rank"
                            name="rank_id"
                            value={user.rank_id}
                            onChange={handleChange}
                        >
                            {ranks.map((rank) => (
                                <MenuItem
                                    key={rank.rank_id}
                                    value={rank.rank_id}
                                >
                                    {rank.rank_name}
                                </MenuItem>
                            ))}
                         </TextField>
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            select
                            label="Unit"
                            name="unit_id"
                            value={user.unit_id}
                            onChange={handleChange}
                        >
                            {units.map((unit) => (
                                <MenuItem
                                    key={unit.unit_id}
                                    value={unit.unit_id}
                                >
                                    {unit.unit_name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>

                </Grid>

            </DialogContent>

            <DialogActions>

                <Button onClick={handleClose}>
                    Cancel
                </Button>

                <Button
                    variant="contained"
                    onClick={handleSubmit}
                >
                    Add User
                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default UserDialog;