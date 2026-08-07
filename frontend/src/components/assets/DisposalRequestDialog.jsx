import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    Typography,
} from "@mui/material";

import { requestDisposal } from "../../services/disposalService";


function DisposalRequestDialog({
    open,
    handleClose,
    asset,
    refreshAssets,
}) {

    const [reason, setReason] = useState("");

    const [loading, setLoading] = useState(false);


    const handleSubmit = async () => {

        if (!asset) {
            return;
        }

        if (!reason.trim()) {

            alert("Please enter a disposal reason.");

            return;

        }


        try {

            setLoading(true);
            
            await requestDisposal({

                asset_id: asset.asset_id,

                reason: reason.trim(),

            });


            alert(
                "Disposal request submitted successfully."
            );


            setReason("");


            if (refreshAssets) {

                await refreshAssets();

            }


            handleClose();

        }
        catch (error) {

            console.error(error);


            alert(
                error?.response?.data?.detail ||
                "Failed to submit disposal request."
            );

        }
        finally {

            setLoading(false);

        }

    };


    const handleDialogClose = () => {

        setReason("");

        handleClose();

    };


    return (

        <Dialog
            open={open}
            onClose={handleDialogClose}
            fullWidth
            maxWidth="sm"
        >

            <DialogTitle>
                Request Asset Disposal
            </DialogTitle>


            <DialogContent>

                <Typography
                    color="text.secondary"
                    sx={{ mb: 2 }}
                >

                    Submit this asset for condemnation
                    and disposal approval.

                </Typography>


                <TextField
                    fullWidth
                    margin="normal"
                    label="Asset"
                    value={
                        asset?.asset_name || ""
                    }
                    disabled
                />


                <TextField
                    fullWidth
                    margin="normal"
                    label="Asset Code"
                    value={
                        asset?.asset_code || ""
                    }
                    disabled
                />


                <TextField
                    fullWidth
                    margin="normal"
                    label="Current Status"
                    value={
                        asset?.status || ""
                    }
                    disabled
                />


                <TextField
                    fullWidth
                    margin="normal"
                    label="Disposal Reason"
                    placeholder="Enter reason for condemnation/disposal"
                    multiline
                    minRows={4}
                    value={reason}
                    onChange={(e) =>
                        setReason(e.target.value)
                    }
                />

            </DialogContent>


            <DialogActions>

                <Button
                    onClick={handleDialogClose}
                    disabled={loading}
                >

                    Cancel

                </Button>


                <Button
                    variant="contained"
                    color="error"
                    onClick={handleSubmit}
                    disabled={
                        loading ||
                        !asset ||
                        !reason.trim()
                    }
                >

                    {loading
                        ? "Submitting..."
                        : "Submit Disposal Request"}

                </Button>

            </DialogActions>

        </Dialog>

    );

}


export default DisposalRequestDialog;