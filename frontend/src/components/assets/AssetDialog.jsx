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
    createAsset,
    updateAsset,
    getAssetCategories,
    getAssetStatuses,
} from "../../services/assetService";

function AssetDialog({
    open,
    handleClose,
    loadAssets,
    selectedAsset,
}) {

    const emptyAsset = {
        asset_code: "",
        asset_name: "",
        category: "",
        manufacturer: "",
        model: "",
        serial_number: "",
        purchase_date: "",
        purchase_price: "",
        current_value: "",
        status: "Available",
        assigned_to: "",
    };

    const [asset, setAsset] = useState(emptyAsset);
    const [categories, setCategories] = useState([]);

    const [statuses, setStatuses] = useState([]);

    useEffect(() => {

        loadMasters();

    }, []);

    const loadMasters = async () => {

        try {

            const categoryData = await getAssetCategories();

            const statusData = await getAssetStatuses();

            setCategories(categoryData);

            setStatuses(statusData);

        }

        catch (err) {

            console.log(err);

        }

    };


    useEffect(() => {

        if (selectedAsset) {

            setAsset({
                asset_code: selectedAsset.asset_code || "",
                asset_name: selectedAsset.asset_name || "",
                category: selectedAsset.category || "",
                manufacturer: selectedAsset.manufacturer || "",
                model: selectedAsset.model || "",
                serial_number: selectedAsset.serial_number || "",
                purchase_date: selectedAsset.purchase_date || "",
                purchase_price: selectedAsset.purchase_price || "",
                current_value: selectedAsset.current_value || "",
                status: selectedAsset.status || "Available",
                assigned_to: selectedAsset.assigned_to || "",
            });

        } else {

            setAsset(emptyAsset);

        }

    }, [selectedAsset, open]);

    const handleChange = (e) => {

        setAsset({
            ...asset,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async () => {

        try {

            const payload = {

                ...asset,

                purchase_date:
                    asset.purchase_date === ""
                        ? null
                        : asset.purchase_date,

                purchase_price:
                    asset.purchase_price === ""
                        ? null
                        : Number(asset.purchase_price),

                current_value:
                    asset.current_value === ""
                        ? null
                        : Number(asset.current_value),

                assigned_to:
                    asset.assigned_to === ""
                        ? null
                        : Number(asset.assigned_to),

            };

            if (selectedAsset) {

                await updateAsset(
                    selectedAsset.asset_id,
                    payload
                );

                alert("Asset Updated Successfully");

            } else {

                await createAsset(payload);

                alert("Asset Created Successfully");

            }

            loadAssets();

            handleClose();

        }
        catch (err) {

            console.log(err);

            if (err.response) {

                alert(JSON.stringify(err.response.data));

            } else {

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

                {selectedAsset
                    ? "Edit Asset"
                    : "Add New Asset"}

            </DialogTitle>

            <DialogContent>

                <Grid
                    container
                    spacing={2}
                    sx={{ mt: 1 }}
                >

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Asset Code"
                            name="asset_code"
                            value={asset.asset_code}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Asset Name"
                            name="asset_name"
                            value={asset.asset_name}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            select
                            label="Category"
                            name="category"
                            value={asset.category}
                            onChange={handleChange}
                        >
                            {categories.map((category) => (
                                <MenuItem
                                    key={category.category_id}
                                    value={category.category_name}
                                >
                                    {category.category_name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Manufacturer"
                            name="manufacturer"
                            value={asset.manufacturer}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Model"
                            name="model"
                            value={asset.model}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            label="Serial Number"
                            name="serial_number"
                            value={asset.serial_number}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            type="date"
                            label="Purchase Date"
                            name="purchase_date"
                            value={asset.purchase_date}
                            onChange={handleChange}
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Purchase Price"
                            name="purchase_price"
                            value={asset.purchase_price}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={4}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Current Value"
                            name="current_value"
                            value={asset.current_value}
                            onChange={handleChange}
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            select
                            label="Status"
                            name="status"
                            value={asset.status}
                            onChange={handleChange}
                        >
                           {statuses.map((status) => (
                                <MenuItem
                                    key={status.status_id}
                                    value={status.status_name}
                                >
                                    {status.status_name}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            fullWidth
                            type="number"
                            label="Assigned To (User ID)"
                            name="assigned_to"
                            value={asset.assigned_to}
                            onChange={handleChange}
                        />
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
                    {selectedAsset
                        ? "Update Asset"
                        : "Add Asset"}
                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default AssetDialog;