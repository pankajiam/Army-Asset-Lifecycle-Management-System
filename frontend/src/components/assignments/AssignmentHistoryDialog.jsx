import { useEffect, useState } from "react";

import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Chip,
    Typography,
} from "@mui/material";

import { getAssetHistory } from "../../services/assignmentService";

function AssignmentHistoryDialog({
    open,
    handleClose,
    assignment,
}) {

    const [history, setHistory] = useState([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (open && assignment) {

            loadHistory();

        }

    }, [open, assignment]);

    const loadHistory = async () => {

        try {

            setLoading(true);

            const data = await getAssetHistory(
                assignment.asset_id
            );

            setHistory(data);

        } catch (error) {

            console.error(error);

            alert("Failed to load assignment history.");

        } finally {

            setLoading(false);

        }

    };

    return (

        <Dialog
            open={open}
            onClose={handleClose}
            fullWidth
            maxWidth="lg"
        >

            <DialogTitle>

                Assignment History

            </DialogTitle>

            <DialogContent>

                <Typography
                    variant="h6"
                    sx={{ mb: 2 }}
                >

                    Asset: {assignment?.asset_name || ""}

                </Typography>

                {loading ? (

                    <Typography>
                        Loading history...
                    </Typography>

                ) : (

                    <TableContainer
                        component={Paper}
                        elevation={2}
                    >

                        <Table>

                            <TableHead>

                                <TableRow>

                                    <TableCell>
                                        <b>User</b>
                                    </TableCell>

                                    <TableCell>
                                        <b>Issued Date</b>
                                    </TableCell>

                                    <TableCell>
                                        <b>Issue Condition</b>
                                    </TableCell>

                                    <TableCell>
                                        <b>Return Date</b>
                                    </TableCell>

                                    <TableCell>
                                        <b>Return Condition</b>
                                    </TableCell>

                                    <TableCell>
                                        <b>Status</b>
                                    </TableCell>

                                </TableRow>

                            </TableHead>

                            <TableBody>

                                {history.map((item) => (

                                    <TableRow
                                        key={item.assignment_id}
                                    >

                                        <TableCell>
                                            {item.user_name ||
                                                item.user_id}
                                        </TableCell>

                                        <TableCell>

                                            {item.issued_at
                                                ? new Date(
                                                    item.issued_at
                                                ).toLocaleDateString()
                                                : "-"}

                                        </TableCell>

                                        <TableCell>
                                            {item.issue_condition || "-"}
                                        </TableCell>

                                        <TableCell>

                                            {item.returned_at
                                                ? new Date(
                                                    item.returned_at
                                                ).toLocaleDateString()
                                                : "-"}

                                        </TableCell>

                                        <TableCell>
                                            {item.return_condition || "-"}
                                        </TableCell>

                                        <TableCell>

                                            <Chip
                                                label={
                                                    item.returned_at
                                                        ? "Returned"
                                                        : "Active"
                                                }
                                                color={
                                                    item.returned_at
                                                        ? "success"
                                                        : "warning"
                                                }
                                                size="small"
                                            />

                                        </TableCell>

                                    </TableRow>

                                ))}

                            </TableBody>

                        </Table>

                    </TableContainer>

                )}

            </DialogContent>

            <DialogActions>

                <Button onClick={handleClose}>

                    Close

                </Button>

            </DialogActions>

        </Dialog>

    );

}

export default AssignmentHistoryDialog;