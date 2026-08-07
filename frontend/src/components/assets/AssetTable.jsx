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
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    Typography,
    Stack,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import QrCode2Icon from "@mui/icons-material/QrCode2";
import DownloadIcon from "@mui/icons-material/Download";
import PrintIcon from "@mui/icons-material/Print";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep";

import DepreciationDialog from "./DepreciationDialog";
import DisposalRequestDialog from "./DisposalRequestDialog";

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

    const [openDepreciationDialog, setOpenDepreciationDialog] =
        useState(false);

    const [openDisposalDialog, setOpenDisposalDialog] =
        useState(false);

    const [qrOpen, setQrOpen] = useState(false);

    const [selectedAsset, setSelectedAsset] = useState(null);

    const [qrUrl, setQrUrl] = useState("");

    const [qrLoading, setQrLoading] = useState(false);


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


    const handleOpenDepreciation = (asset) => {

        setSelectedAsset(asset);

        setOpenDepreciationDialog(true);

    };


    const handleCloseDepreciation = () => {

        setOpenDepreciationDialog(false);

        setSelectedAsset(null);

    };


    const handleOpenDisposal = (asset) => {

        setSelectedAsset(asset);

        setOpenDisposalDialog(true);

    };


    const handleCloseDisposal = () => {

        setOpenDisposalDialog(false);

        setSelectedAsset(null);

    };


    const handleOpenQR = async (asset) => {

        try {

            setQrLoading(true);

            setSelectedAsset(asset);

            setQrOpen(true);

            const token = localStorage.getItem("token");

            const response = await fetch(
                `http://127.0.0.1:8000/assets/${asset.asset_id}/qr`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );


            if (!response.ok) {

                throw new Error(
                    "Failed to generate QR code"
                );

            }


            const blob = await response.blob();

            const imageUrl = URL.createObjectURL(blob);

            setQrUrl(imageUrl);

        }
        catch (error) {

            console.error(error);

            alert("Failed to load QR code.");

            setQrOpen(false);

        }
        finally {

            setQrLoading(false);

        }

    };


    const handleCloseQR = () => {

        if (qrUrl) {

            URL.revokeObjectURL(qrUrl);

        }

        setQrUrl("");

        setSelectedAsset(null);

        setQrOpen(false);

    };


    const handleDownloadQR = () => {

        if (!qrUrl || !selectedAsset) {

            return;

        }


        const link = document.createElement("a");

        link.href = qrUrl;

        link.download =
            `${selectedAsset.asset_code}_QR.png`;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

    };


    const handlePrintQR = () => {

        if (!qrUrl || !selectedAsset) {

            return;

        }


        const printWindow = window.open(
            "",
            "_blank",
            "width=600,height=700"
        );


        if (!printWindow) {

            alert(
                "Please allow pop-ups to print the QR code."
            );

            return;

        }


        printWindow.document.write(`

            <html>

                <head>

                    <title>
                        ${selectedAsset.asset_code} QR Code
                    </title>

                    <style>

                        body {
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding: 40px;
                        }

                        img {
                            width: 300px;
                            height: 300px;
                        }

                        h2 {
                            margin-bottom: 8px;
                        }

                        p {
                            margin-top: 4px;
                        }

                    </style>

                </head>

                <body>

                    <h2>
                        ${selectedAsset.asset_name}
                    </h2>

                    <p>
                        Asset Code:
                        ${selectedAsset.asset_code}
                    </p>

                    <img
                        src="${qrUrl}"
                        alt="Asset QR Code"
                    />

                    <script>

                        window.onload = function () {
                            window.print();
                        };

                    <\/script>

                </body>

            </html>

        `);


        printWindow.document.close();

    };


    return (

        <>

            <TableContainer
                component={Paper}
                elevation={3}
                sx={{ mt: 3 }}
            >

                <Table>

                    <TableHead>

                        <TableRow>

                            <TableCell>
                                <b>Asset Code</b>
                            </TableCell>

                            <TableCell>
                                <b>Asset Name</b>
                            </TableCell>

                            <TableCell>
                                <b>Category</b>
                            </TableCell>

                            <TableCell>
                                <b>Status</b>
                            </TableCell>

                            <TableCell>
                                <b>Actions</b>
                            </TableCell>

                        </TableRow>

                    </TableHead>


                    <TableBody>

                        {rows.map((row) => (

                            <TableRow
                                key={row.asset_id}
                                hover
                            >

                                <TableCell>
                                    {row.asset_code}
                                </TableCell>

                                <TableCell>
                                    {row.asset_name}
                                </TableCell>

                                <TableCell>
                                    {row.category}
                                </TableCell>

                                <TableCell>

                                    <Chip
                                        label={row.status}
                                        color={statusColor(row.status)}
                                        size="small"
                                    />

                                </TableCell>


                                <TableCell>

                                    <IconButton
                                        color="primary"
                                    >

                                        <VisibilityIcon />

                                    </IconButton>


                                    <IconButton
                                        color="secondary"
                                        onClick={() =>
                                            handleOpenQR(row)
                                        }
                                    >

                                        <QrCode2Icon />

                                    </IconButton>


                                    <IconButton
                                        color="warning"
                                        onClick={() =>
                                            handleEdit(row)
                                        }
                                    >

                                        <EditIcon />

                                    </IconButton>


                                    <IconButton
                                        color="success"
                                        onClick={() =>
                                            handleOpenDepreciation(row)
                                        }
                                    >

                                        <AccountBalanceWalletIcon />

                                    </IconButton>


                                    <IconButton
                                        color="error"
                                        onClick={() =>
                                            handleOpenDisposal(row)
                                        }
                                    >

                                        <DeleteSweepIcon />

                                    </IconButton>

                                </TableCell>


                            </TableRow>

                        ))}

                    </TableBody>

                </Table>

            </TableContainer>


            <Dialog
                open={qrOpen}
                onClose={handleCloseQR}
                maxWidth="sm"
                fullWidth
            >

                <DialogTitle>
                    Asset QR Code
                </DialogTitle>


                <DialogContent
                    sx={{
                        textAlign: "center",
                        py: 4,
                    }}
                >

                    {selectedAsset && (

                        <>

                            <Typography
                                variant="h6"
                                sx={{ mb: 1 }}
                            >

                                {selectedAsset.asset_name}

                            </Typography>


                            <Typography
                                color="text.secondary"
                                sx={{ mb: 3 }}
                            >

                                Asset Code:{" "}
                                {selectedAsset.asset_code}

                            </Typography>


                            {qrLoading ? (

                                <Typography>
                                    Generating QR Code...
                                </Typography>

                            ) : qrUrl ? (

                                <img
                                    src={qrUrl}
                                    alt="Asset QR Code"
                                    style={{
                                        width: "300px",
                                        height: "300px",
                                    }}
                                />

                            ) : (

                                <Typography>
                                    QR Code unavailable.
                                </Typography>

                            )}

                        </>

                    )}

                </DialogContent>


                <DialogActions>

                    <Stack
                        direction="row"
                        spacing={1}
                        sx={{
                            width: "100%",
                            justifyContent: "flex-end",
                        }}
                    >

                        <Button
                            variant="outlined"
                            startIcon={<DownloadIcon />}
                            onClick={handleDownloadQR}
                            disabled={!qrUrl || qrLoading}
                        >

                            Download QR

                        </Button>


                        <Button
                            variant="contained"
                            startIcon={<PrintIcon />}
                            onClick={handlePrintQR}
                            disabled={!qrUrl || qrLoading}
                        >

                            Print QR

                        </Button>


                        <Button
                            onClick={handleCloseQR}
                        >

                            Close

                        </Button>

                    </Stack>

                </DialogActions>

            </Dialog>


            <DepreciationDialog
                open={openDepreciationDialog}
                handleClose={handleCloseDepreciation}
                asset={selectedAsset}
                refreshAssets={fetchAssets}
            />


            <DisposalRequestDialog
                open={openDisposalDialog}
                handleClose={handleCloseDisposal}
                asset={selectedAsset}
                refreshAssets={fetchAssets}
            />

        </>

    );

}


export default AssetTable;