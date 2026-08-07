import { useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    TextField,
    Typography,
    Box,
    Divider,
} from "@mui/material";

import { depreciateAsset } from "../../services/assetService";

function DepreciationDialog({
    open,
    handleClose,
    asset,
    refreshAssets,
}) {

    const [loading, setLoading] = useState(false);

    const [updatedAsset, setUpdatedAsset] = useState(null);

    const handleCalculate = async () => {

        if (!asset) {
            return;
        }

        try {

            setLoading(true);

            const result = await depreciateAsset(
                asset.asset_id
            );

            setUpdatedAsset(result);

            if (refreshAssets) {
                await refreshAssets();
            }

        }
        catch (error) {

            console.error(error);

            alert(
                error?.response?.data?.detail ||
                "Failed to calculate depreciation."
            );

        }
        finally {

            setLoading(false);

        }

    };

    const displayAsset =
        updatedAsset || asset;

    const purchasePrice =
        displayAsset?.purchase_price != null
            ? Number(displayAsset.purchase_price)
            : null;

    const currentValue =
        displayAsset?.current_value != null
            ? Number(displayAsset.current_value)
            : null;

    const depreciationAmount =
        purchasePrice !== null &&
        currentValue !== null
            ? purchasePrice - currentValue
            : null;

    const formatCurrency = (value) => {

        if (value === null || value === undefined) {
            return "Not available";
        }

        return `₹${value.toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        })}`;

    };

    const handleDialogClose = () => {

        setUpdatedAsset(null);

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
                Asset Depreciation
            </DialogTitle>

            <DialogContent>

                <TextField
                    fullWidth
                    margin="normal"
                    label="Asset"
                    value={
                        displayAsset?.asset_name || ""
                    }
                    disabled
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Asset Code"
                    value={
                        displayAsset?.asset_code || ""
                    }
                    disabled
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Purchase Date"
                    value={
                        displayAsset?.purchase_date
                            ? new Date(
                                displayAsset.purchase_date
                            ).toLocaleDateString()
                            : "Not available"
                    }
                    disabled
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Purchase Price"
                    value={formatCurrency(purchasePrice)}
                    disabled
                />

                <Divider sx={{ my: 2 }} />

                <Box
                    sx={{
                        p: 2,
                        borderRadius: 2,
                        bgcolor: "action.hover",
                    }}
                >

                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        Depreciation Rate
                    </Typography>

                    <Typography
                        variant="h6"
                        fontWeight="bold"
                    >
                        10% per year
                    </Typography>

                    <Typography
                        variant="caption"
                        color="text.secondary"
                    >
                        Current backend depreciation rule
                    </Typography>

                </Box>

                <Box sx={{ mt: 2 }}>

                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        Current Value
                    </Typography>

                    <Typography
                        variant="h5"
                        fontWeight="bold"
                        color="primary"
                    >
                        {formatCurrency(currentValue)}
                    </Typography>

                </Box>

                {depreciationAmount !== null && (

                    <Box sx={{ mt: 2 }}>

                        <Typography
                            variant="body2"
                            color="text.secondary"
                        >
                            Total Depreciation
                        </Typography>

                        <Typography
                            variant="h6"
                            fontWeight="bold"
                            color="error"
                        >
                            {formatCurrency(
                                depreciationAmount
                            )}
                        </Typography>

                    </Box>

                )}

            </DialogContent>

            <DialogActions>

                <Button
                    onClick={handleDialogClose}
                >
                    Close
                </Button>

                <Button
                    variant="contained"
                    onClick={handleCalculate}
                    disabled={loading || !asset}
                >
                    {loading
                        ? "Calculating..."
                        : "Calculate Depreciation"}
                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default DepreciationDialog;