import {
    Box,
    Button,
    Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

function AssignmentToolbar({

    handleOpenIssue,

}) {

    return (

        <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            sx={{ mt: 3 }}
        >

            <Typography
                variant="h5"
                fontWeight="bold"
            >
                Asset Assignments
            </Typography>

            <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleOpenIssue}
            >
                Issue Asset
            </Button>

        </Box>

    );

}

export default AssignmentToolbar;