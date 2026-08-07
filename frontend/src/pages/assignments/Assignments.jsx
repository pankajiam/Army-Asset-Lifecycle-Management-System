import { useState } from "react";

import Sidebar from "../../components/layout/Sidebar";

import AssignmentToolbar from "../../components/assignments/AssignmentToolbar";
import AssignmentTable from "../../components/assignments/AssignmentTable";
import IssueAssetDialog from "../../components/assignments/IssueAssetDialog";
import ReturnAssetDialog from "../../components/assignments/ReturnAssetDialog";

import {
    Box,
    Toolbar,
    Typography,
} from "@mui/material";

function Assignments() {

    const [openIssueDialog, setOpenIssueDialog] = useState(false);

    const [openReturnDialog, setOpenReturnDialog] = useState(false);

    const [selectedAssignment, setSelectedAssignment] = useState(null);

    const handleOpenIssue = () => {
        setOpenIssueDialog(true);
    };

    const handleCloseIssue = () => {
        setOpenIssueDialog(false);
    };

    const handleOpenReturn = (assignment) => {

        setSelectedAssignment(assignment);

        setOpenReturnDialog(true);

    };

    const handleCloseReturn = () => {

        setOpenReturnDialog(false);

        setSelectedAssignment(null);

    };

    const refreshAssignments = () => {

        window.location.reload();

    };

    return (

        <Box sx={{ display: "flex" }}>

            <Sidebar />

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
                >
                    Assignment Management
                </Typography>

                <Typography
                    color="text.secondary"
                    sx={{ mt: 1, mb: 3 }}
                >
                    Issue, Return and Transfer Army Assets
                </Typography>

                <AssignmentToolbar
                    handleOpenIssue={handleOpenIssue}
                />

                <AssignmentTable
                    handleOpenReturn={handleOpenReturn}
                />

                <IssueAssetDialog
                    open={openIssueDialog}
                    handleClose={handleCloseIssue}
                    refreshAssignments={refreshAssignments}
                />

                <ReturnAssetDialog
                    open={openReturnDialog}
                    handleClose={handleCloseReturn}
                    assignment={selectedAssignment}
                    refreshAssignments={refreshAssignments}
                />

            </Box>

        </Box>

    );

}

export default Assignments;