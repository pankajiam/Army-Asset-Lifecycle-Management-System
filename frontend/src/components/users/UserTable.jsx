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

function UserTable({ users }) {

    return (

        <TableContainer
            component={Paper}
            elevation={3}
            sx={{ mt: 3 }}
        >

            <Table>

                <TableHead>

                    <TableRow>

                        <TableCell><b>Army Number</b></TableCell>

                        <TableCell><b>First Name</b></TableCell>

                        <TableCell><b>Last Name</b></TableCell>

                        <TableCell><b>Email</b></TableCell>

                        <TableCell><b>Phone</b></TableCell>

                        <TableCell><b>Status</b></TableCell>

                        <TableCell align="center"><b>Actions</b></TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {users.map((user) => (

                        <TableRow
                            key={user.user_id}
                            hover
                        >

                            <TableCell>{user.army_number}</TableCell>

                            <TableCell>{user.first_name}</TableCell>

                            <TableCell>{user.last_name}</TableCell>

                            <TableCell>{user.email}</TableCell>

                            <TableCell>{user.phone}</TableCell>

                            <TableCell>

                                <Chip
                                    label="Active"
                                    color="success"
                                    size="small"
                                />

                            </TableCell>

                            <TableCell align="center">

                                <IconButton color="primary">
                                    <VisibilityIcon />
                                </IconButton>

                                <IconButton color="warning">
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

export default UserTable;