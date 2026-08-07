import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    MenuItem,
} from "@mui/material";

import { returnAsset } from "../../services/assignmentService";

function ReturnAssetDialog({

    open,
    handleClose,
    assignment,
    refreshAssignments,

}) {

    const [returnCondition, setReturnCondition] = useState("Good");

    const handleSubmit = async () => {

        try {

            await returnAsset({

                asset_id: assignment.asset_id,

                return_condition: returnCondition,

            });

            alert("Asset Returned Successfully");

            refreshAssignments();

            handleClose();

        }

        catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.detail ||
                "Failed to return asset."
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

                Return Asset

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
                    label="Return Condition"
                    value={returnCondition}
                    onChange={(e) =>
                        setReturnCondition(e.target.value)
                    }
                    margin="normal"
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
                    color="success"
                    onClick={handleSubmit}
                >

                    Return Asset

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default ReturnAssetDialog;