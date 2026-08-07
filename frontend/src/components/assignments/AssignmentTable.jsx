import { useEffect, useState } from "react";

import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    IconButton,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import AssignmentReturnIcon from "@mui/icons-material/AssignmentReturn";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";

import { getAssignments } from "../../services/assignmentService";

function AssignmentTable({

    handleOpenReturn,

}) {

    const [assignments, setAssignments] = useState([]);

    useEffect(() => {

        loadAssignments();

    }, []);

    const loadAssignments = async () => {

        try {

            const data = await getAssignments();

            setAssignments(data);

        } catch (error) {

            console.error(error);

            alert("Failed to load assignments.");

        }

    };

    return (

        <TableContainer
            component={Paper}
            elevation={3}
            sx={{ mt: 3 }}
        >

            <Table>

                <TableHead>

                    <TableRow>

                        <TableCell><b>Asset</b></TableCell>

                        <TableCell><b>User</b></TableCell>

                        <TableCell><b>Issue Date</b></TableCell>

                        <TableCell><b>Condition</b></TableCell>

                        <TableCell><b>Status</b></TableCell>

                        <TableCell align="center">

                            <b>Actions</b>

                        </TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {assignments.map((assignment) => (

                        <TableRow
                            key={assignment.assignment_id}
                            hover
                        >

                            <TableCell>

                                {assignment.asset_name}

                            </TableCell>

                            <TableCell>

                                {assignment.user_name}

                            </TableCell>

                            <TableCell>

                                {new Date(
                                    assignment.issued_at
                                ).toLocaleDateString()}

                            </TableCell>

                            <TableCell>

                                {assignment.issue_condition}

                            </TableCell>

                            <TableCell>

                                <Chip
                                    label={
                                        assignment.returned_at
                                            ? "Returned"
                                            : "Issued"
                                    }
                                    color={
                                        assignment.returned_at
                                            ? "success"
                                            : "warning"
                                    }
                                    size="small"
                                />

                            </TableCell>

                            <TableCell align="center">

                                <IconButton
                                    color="primary"
                                >

                                    <VisibilityIcon />

                                </IconButton>

                                <IconButton
                                    color="success"
                                    onClick={() =>
                                        handleOpenReturn(
                                            assignment
                                        )
                                    }
                                >

                                    <AssignmentReturnIcon />

                                </IconButton>

                                <IconButton
                                    color="warning"
                                >

                                    <SwapHorizIcon />

                                </IconButton>

                            </TableCell>

                        </TableRow>

                    ))}

                </TableBody>

            </Table>

        </TableContainer>

    );

}

export default AssignmentTable;