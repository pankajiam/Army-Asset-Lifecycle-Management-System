import {
    Box,
    Button,
    MenuItem,
    TextField,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

function UserToolbar({ handleOpen }) {

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
                    label="Search User"
                    placeholder="Army ID / Name"
                    sx={{ minWidth: 250 }}
                />

                <TextField
                    select
                    size="small"
                    label="Role"
                    defaultValue=""
                    sx={{ minWidth: 180 }}
                >

                    <MenuItem value="">
                        All
                    </MenuItem>

                    <MenuItem value="Admin">
                        Admin
                    </MenuItem>

                    <MenuItem value="Officer">
                        Officer
                    </MenuItem>

                    <MenuItem value="Soldier">
                        Soldier
                    </MenuItem>

                </TextField>

                <TextField
                    select
                    size="small"
                    label="Rank"
                    defaultValue=""
                    sx={{ minWidth: 180 }}
                >

                    <MenuItem value="">
                        All
                    </MenuItem>

                    <MenuItem value="Captain">
                        Captain
                    </MenuItem>

                    <MenuItem value="Major">
                        Major
                    </MenuItem>

                    <MenuItem value="Colonel">
                        Colonel
                    </MenuItem>

                </TextField>

            </Box>

            <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleOpen}
            >
                Add User
            </Button>

        </Box>

    );

}

export default UserToolbar;