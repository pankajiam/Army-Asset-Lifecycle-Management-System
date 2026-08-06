import { useState } from "react";

import { Box, Toolbar, Typography } from "@mui/material";

import Sidebar from "../../components/layout/Sidebar";
import Navbar from "../../components/layout/Navbar";

import AssetToolbar from "../../components/assets/AssetToolbar";
import AssetTable from "../../components/assets/AssetTable";
import AssetDialog from "../../components/assets/AssetDialog";

function Assets() {

    const [openDialog, setOpenDialog] = useState(false);

    const [selectedAsset, setSelectedAsset] = useState(null);

    const [loadAssets, setLoadAssets] = useState(0);

    const handleOpen = () => {

        setSelectedAsset(null);

        setOpenDialog(true);

    };

    const handleClose = () => {

        setOpenDialog(false);

        setSelectedAsset(null);

    };

    const handleEdit = (asset) => {

        setSelectedAsset(asset);

        setOpenDialog(true);

    };

    const refreshAssets = () => {

        setLoadAssets(prev => prev + 1);

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
                    Asset Management
                </Typography>

                <AssetToolbar
                    handleOpen={handleOpen}
                />

                <AssetTable
                    loadAssets={loadAssets}
                    handleEdit={handleEdit}
                />

                <AssetDialog
                    open={openDialog}
                    handleClose={handleClose}
                    loadAssets={refreshAssets}
                    selectedAsset={selectedAsset}
                />

            </Box>

        </Box>

    );

}

export default Assets;