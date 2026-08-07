import { useEffect, useState } from "react";
import { getAssets } from "../../services/assetService";
import { getUsers } from "../../services/userService";
import { issueAsset } from "../../services/assignmentService";

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

function IssueAssetDialog({

    open,
    handleClose,
    refreshAssignments,

}) {

    const [assets, setAssets] = useState([]);

    const [users, setUsers] = useState([]);

    const [assignment, setAssignment] = useState({

        asset_id: "",

        user_id: "",

        issue_condition: "Good",

    });

    useEffect(() => {

        if (open) {

            loadData();

        }

    }, [open]);

    const loadData = async () => {

        try {

            const assetData = await getAssets();

            const userData = await getUsers();

            // Show only available assets
            setAssets(
                assetData.filter(
                    (asset) => asset.status === "Available"
                )
            );

            
            setUsers(userData);

        } catch (error) {

            console.error(error);

            alert("Failed to load Assets or Users.");

        }

    };

    const handleChange = (e) => {

        setAssignment({

            ...assignment,

            [e.target.name]: e.target.value,

        });

    };

    const handleSubmit = async () => {

        try {

            await issueAsset(assignment);

            alert("Asset Issued Successfully");

            refreshAssignments();

            handleClose();

        } catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.detail ||
                "Failed to issue asset."
            );

        }

    };

    return (

        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>

                Issue Asset

            </DialogTitle>

            <DialogContent>

                <Grid
                    container
                    spacing={2}
                    sx={{ mt: 1 }}
                >

                    <Grid size ={12}>

                        <TextField
                            fullWidth
                            select
                            label="Asset"
                            name="asset_id"
                            value={assignment.asset_id}
                            onChange={handleChange}
                        >

                            {assets.map((asset) => (

                                <MenuItem
                                    key={asset.asset_id}
                                    value={asset.asset_id}
                                >

                                    {asset.asset_name}

                                </MenuItem>

                            ))}

                        </TextField>

                    </Grid>

                    <Grid size ={12}>

                        <TextField
                            fullWidth
                            select
                            label="User"
                            name="user_id"
                            value={assignment.user_id}
                            onChange={handleChange}
                        >

                            {users.map((user) => (

                                <MenuItem
                                    key={user.user_id}
                                    value={user.user_id}
                                >

                                    {user.first_name} {user.last_name}

                                </MenuItem>

                            ))}

                        </TextField>

                    </Grid>

                    <Grid size ={12}>

                        <TextField
                            fullWidth
                            select
                            label="Issue Condition"
                            name="issue_condition"
                            value={assignment.issue_condition}
                            onChange={handleChange}
                        >

                            <MenuItem value="Excellent">
                                Excellent
                            </MenuItem>

                            <MenuItem value="Good">
                                Good
                            </MenuItem>

                            <MenuItem value="Fair">
                                Fair
                            </MenuItem>

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

                    Issue Asset

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default IssueAssetDialog;