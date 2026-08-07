import { useEffect, useState } from "react";

import {
    Box,
    Paper,
    Typography,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Button,
    CircularProgress,
    Alert,
} from "@mui/material";

import {
    getPendingDisposals,
    approveDisposal,
} from "../../services/disposalService";


function DisposalApproval() {

    const [disposals, setDisposals] = useState([]);

    const [loading, setLoading] = useState(true);

    const [approvingId, setApprovingId] = useState(null);

    const [error, setError] = useState("");


    const loadDisposals = async () => {

        try {

            setLoading(true);

            setError("");

            const data = await getPendingDisposals();

            setDisposals(data);

        }
        catch (err) {

            console.error(err);

            setError(
                err?.response?.data?.detail ||
                "Failed to load pending disposal requests."
            );

        }
        finally {

            setLoading(false);

        }

    };


    useEffect(() => {

        loadDisposals();

    }, []);


    const handleApprove = async (disposalId) => {

        const confirmed = window.confirm(
            "Are you sure you want to approve this disposal request?"
        );

        if (!confirmed) {

            return;

        }


        try {

            setApprovingId(disposalId);

            setError("");

            await approveDisposal(disposalId);

            alert(
                "Disposal request approved successfully."
            );

            await loadDisposals();

        }
        catch (err) {

            console.error(err);

            setError(
                err?.response?.data?.detail ||
                "Failed to approve disposal request."
            );

        }
        finally {

            setApprovingId(null);

        }

    };


    return (

        <Box sx={{ p: 3 }}>

            <Typography
                variant="h4"
                sx={{ mb: 3, fontWeight: 600 }}
            >
                Asset Disposal Approval
            </Typography>


            <Paper
                elevation={3}
                sx={{ p: 2 }}
            >

                <Typography
                    variant="h6"
                    sx={{ mb: 2 }}
                >
                    Pending Disposal Requests
                </Typography>


                {error && (

                    <Alert
                        severity="error"
                        sx={{ mb: 2 }}
                    >
                        {error}
                    </Alert>

                )}


                {loading ? (

                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "center",
                            p: 4,
                        }}
                    >

                        <CircularProgress />

                    </Box>

                ) : disposals.length === 0 ? (

                    <Typography
                        color="text.secondary"
                        sx={{ p: 3 }}
                    >
                        No pending disposal requests.
                    </Typography>

                ) : (

                    <Table>

                        <TableHead>

                            <TableRow>

                                <TableCell>
                                    Disposal ID
                                </TableCell>

                                <TableCell>
                                    Asset ID
                                </TableCell>

                                <TableCell>
                                    Requested By
                                </TableCell>

                                <TableCell>
                                    Reason
                                </TableCell>

                                <TableCell>
                                    Requested At
                                </TableCell>

                                <TableCell>
                                    Status
                                </TableCell>

                                <TableCell>
                                    Action
                                </TableCell>

                            </TableRow>

                        </TableHead>


                        <TableBody>

                            {disposals.map((disposal) => (

                                <TableRow
                                    key={disposal.disposal_id}
                                >

                                    <TableCell>
                                        {disposal.disposal_id}
                                    </TableCell>

                                    <TableCell>
                                        {disposal.asset_id}
                                    </TableCell>

                                    <TableCell>
                                        {disposal.requested_by}
                                    </TableCell>

                                    <TableCell>
                                        {disposal.reason}
                                    </TableCell>

                                    <TableCell>
                                        {disposal.requested_at
                                            ? new Date(
                                                disposal.requested_at
                                            ).toLocaleString()
                                            : "-"
                                        }
                                    </TableCell>

                                    <TableCell>
                                        {disposal.status}
                                    </TableCell>

                                    <TableCell>

                                        <Button
                                            variant="contained"
                                            color="success"
                                            onClick={() =>
                                                handleApprove(
                                                    disposal.disposal_id
                                                )
                                            }
                                            disabled={
                                                approvingId ===
                                                disposal.disposal_id
                                            }
                                        >

                                            {approvingId ===
                                            disposal.disposal_id
                                                ? "Approving..."
                                                : "Approve"
                                            }

                                        </Button>

                                    </TableCell>

                                </TableRow>

                            ))}

                        </TableBody>

                    </Table>

                )}

            </Paper>

        </Box>

    );

}


export default DisposalApproval;