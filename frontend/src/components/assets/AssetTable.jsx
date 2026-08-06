import { useEffect, useState } from "react";

import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    IconButton,
    Chip,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import { getAssets } from "../../services/assetService";

function statusColor(status) {

    switch (status) {

        case "Available":
            return "success";

        case "Assigned":
            return "primary";

        case "Maintenance":
            return "warning";

        case "Disposed":
            return "error";

        default:
            return "default";

    }

}

function AssetTable({ loadAssets, handleEdit }) {

    const [rows, setRows] = useState([]);

    useEffect(() => {

        fetchAssets();

    }, [loadAssets]);

    const fetchAssets = async () => {

        try {

            const data = await getAssets();

            setRows(data);

        }
        catch (err) {

            console.log(err);

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

                        <TableCell><b>Asset Code</b></TableCell>
                        <TableCell><b>Asset Name</b></TableCell>
                        <TableCell><b>Category</b></TableCell>
                        <TableCell><b>Status</b></TableCell>
                        <TableCell><b>Actions</b></TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {rows.map((row) => (

                        <TableRow
                            key={row.asset_id}
                            hover
                        >

                            <TableCell>{row.asset_code}</TableCell>

                            <TableCell>{row.asset_name}</TableCell>

                            <TableCell>{row.category}</TableCell>

                            <TableCell>

                                <Chip
                                    label={row.status}
                                    color={statusColor(row.status)}
                                    size="small"
                                />

                            </TableCell>

                            <TableCell>

                                <IconButton color="primary">

                                    <VisibilityIcon />

                                </IconButton>

                                <IconButton
                                    color="warning"
                                    onClick={() => handleEdit(row)}
                                >

                                    <EditIcon />

                                </IconButton>

                                <IconButton color="error">

                                    <DeleteIcon />

                                </IconButton>

                            </TableCell>

                        </TableRow>

                    ))}

                </TableBody>

            </Table>

        </TableContainer>

    );

}

export default AssetTable;