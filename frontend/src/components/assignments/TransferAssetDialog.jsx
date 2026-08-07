import { useEffect, useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    MenuItem,
} from "@mui/material";

import { getUsers } from "../../services/userService";
import { transferAsset } from "../../services/assignmentService";

function TransferAssetDialog({

    open,
    handleClose,
    assignment,
    refreshAssignments,

}) {

    const [users, setUsers] = useState([]);

    const [newUserId, setNewUserId] = useState("");

    const [transferCondition, setTransferCondition] = useState("Good");

    useEffect(() => {

        if (open) {

            loadUsers();

            setNewUserId("");

            setTransferCondition("Good");

        }

    }, [open]);

    const loadUsers = async () => {

        try {

            const data = await getUsers();

            setUsers(data);

        } catch (error) {

            console.error(error);

            alert("Failed to load users.");

        }

    };

    const handleSubmit = async () => {

        if (!newUserId) {

            alert("Please select a new user.");

            return;

        }

        try {

            await transferAsset({

                asset_id: assignment.asset_id,

                new_user_id: Number(newUserId),

                transfer_condition: transferCondition,

            });

            alert("Asset Transferred Successfully");

            refreshAssignments();

            handleClose();

        } catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.detail ||
                "Failed to transfer asset."
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

                Transfer Asset

            </DialogTitle>

            <DialogContent>

                <TextField
                    fullWidth
                    margin="normal"
                    label="Asset"
                    value={assignment?.asset_name || ""}
                    disabled
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Current Holder"
                    value={assignment?.user_name || ""}
                    disabled
                />

                <TextField
                    fullWidth
                    select
                    margin="normal"
                    label="Transfer To"
                    value={newUserId}
                    onChange={(e) =>
                        setNewUserId(e.target.value)
                    }
                >

                    {users
                        .filter(
                            (user) =>
                                user.user_id !== assignment?.user_id
                        )
                        .map((user) => (

                            <MenuItem
                                key={user.user_id}
                                value={user.user_id}
                            >

                                {user.first_name} {user.last_name}

                            </MenuItem>

                        ))}

                </TextField>

                <TextField
                    fullWidth
                    select
                    margin="normal"
                    label="Transfer Condition"
                    value={transferCondition}
                    onChange={(e) =>
                        setTransferCondition(e.target.value)
                    }
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

                    <MenuItem value="Damaged">
                        Damaged
                    </MenuItem>

                </TextField>

            </DialogContent>

            <DialogActions>

                <Button onClick={handleClose}>

                    Cancel

                </Button>

                <Button
                    variant="contained"
                    color="warning"
                    onClick={handleSubmit}
                >

                    Transfer Asset

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default TransferAssetDialog;