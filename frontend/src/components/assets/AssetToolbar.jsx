import {
    Box,
    Button,
    MenuItem,
    TextField,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

function AssetToolbar({ handleOpen }) {

    return (

        <Box
            sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexWrap: "wrap",
                gap: 2,
                mb: 3,
            }}
        >

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    flexWrap: "wrap",
                }}
            >

                <TextField
                    size="small"
                    label="Search Asset"
                    placeholder="Asset Name / Asset ID"
                    sx={{ minWidth: 250 }}
                />

                <TextField
                    select
                    size="small"
                    label="Category"
                    defaultValue=""
                    sx={{ minWidth: 180 }}
                >
                    <MenuItem value="">
                        All
                    </MenuItem>

                    <MenuItem value="Weapon">
                        Weapon
                    </MenuItem>

                    <MenuItem value="Vehicle">
                        Vehicle
                    </MenuItem>

                    <MenuItem value="IT Equipment">
                        IT Equipment
                    </MenuItem>

                    <MenuItem value="Communication">
                        Communication
                    </MenuItem>

                </TextField>

                <TextField
                    select
                    size="small"
                    label="Status"
                    defaultValue=""
                    sx={{ minWidth: 180 }}
                >

                    <MenuItem value="">
                        All
                    </MenuItem>

                    <MenuItem value="Available">
                        Available
                    </MenuItem>

                    <MenuItem value="Assigned">
                        Assigned
                    </MenuItem>

                    <MenuItem value="Maintenance">
                        Maintenance
                    </MenuItem>

                    <MenuItem value="Disposed">
                        Disposed
                    </MenuItem>

                </TextField>

            </Box>

            <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleOpen}
            >
                Add Asset
            </Button>

        </Box>

    );

}

export default AssetToolbar;