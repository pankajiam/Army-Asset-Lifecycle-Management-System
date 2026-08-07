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
    CircularProgress,
    Alert,
    Chip,
} from "@mui/material";

import { getAuditLogs } from "../../services/auditLogService";


function AuditLogs() {

    const [logs, setLogs] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    const loadAuditLogs = async () => {

        try {

            setLoading(true);

            setError("");

            const data = await getAuditLogs();

            setLogs(data);

        }
        catch (err) {

            console.error(err);

            setError(
                err?.response?.data?.detail ||
                "Failed to load audit logs."
            );

        }
        finally {

            setLoading(false);

        }

    };


    useEffect(() => {

        loadAuditLogs();

    }, []);


    return (

        <Box sx={{ p: 3 }}>

            <Typography
                variant="h4"
                sx={{
                    mb: 3,
                    fontWeight: 600,
                }}
            >
                Audit Logs
            </Typography>


            <Paper
                elevation={3}
                sx={{ p: 2 }}
            >

                <Typography
                    variant="h6"
                    sx={{ mb: 2 }}
                >
                    System Activity History
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

                ) : logs.length === 0 ? (

                    <Typography
                        color="text.secondary"
                        sx={{ p: 3 }}
                    >
                        No audit logs found.
                    </Typography>

                ) : (

                    <Table>

                        <TableHead>

                            <TableRow>

                                <TableCell>
                                    Audit ID
                                </TableCell>

                                <TableCell>
                                    User ID
                                </TableCell>

                                <TableCell>
                                    Asset ID
                                </TableCell>

                                <TableCell>
                                    Action
                                </TableCell>

                                <TableCell>
                                    Remarks
                                </TableCell>

                                <TableCell>
                                    Date & Time
                                </TableCell>

                            </TableRow>

                        </TableHead>


                        <TableBody>

                            {logs.map((log) => (

                                <TableRow
                                    key={log.audit_id}
                                >

                                    <TableCell>
                                        {log.audit_id}
                                    </TableCell>

                                    <TableCell>
                                        {log.user_id}
                                    </TableCell>

                                    <TableCell>
                                        {log.asset_id ?? "-"}
                                    </TableCell>

                                    <TableCell>

                                        <Chip
                                            label={log.action}
                                            color={
                                                log.action ===
                                                "Approved Disposal"
                                                    ? "success"
                                                    : "primary"
                                            }
                                            size="small"
                                        />

                                    </TableCell>

                                    <TableCell>
                                        {log.remarks || "-"}
                                    </TableCell>

                                    <TableCell>
                                        {log.created_at
                                            ? new Date(
                                                log.created_at
                                            ).toLocaleString()
                                            : "-"
                                        }
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


export default AuditLogs;