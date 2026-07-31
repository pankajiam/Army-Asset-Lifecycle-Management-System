import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    Box,
    Paper,
    Typography,
    TextField,
    Button,
    Alert,
    CircularProgress
} from "@mui/material";

import "./Login.css";
import { login } from "../../services/authService";

function Login() {

    const navigate = useNavigate();

    const [armyNumber, setArmyNumber] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await login(
                armyNumber,
                password
            );

            localStorage.setItem(
                "token",
                response.access_token
            );

            alert("Login Successful");

            console.log(response);
            console.log("Token:", response.access_token);

            navigate("/dashboard");
        

        }
        catch (err) {

            console.log("========== ERROR ==========");
            console.log(err);

            if (err.response) {

                console.log("Status:", err.response.status);
                console.log("Data:", err.response.data);

                alert(
                    "Status: " +
                err.response.status +
                "\n\n" +
                JSON.stringify(err.response.data)
                );

            }
            else {

                    console.log("No response received");
                    alert(err.message);

            }

            setError("Invalid Army Number or Password");

        }
        finally {

            setLoading(false);

        }

    };

    return (

        <Box className="login-container">

            <Paper
                elevation={5}
                className="login-card"
            >

                <Box className="logo">

                    <Typography
                        variant="h4"
                        color="primary"
                    >
                        🇮🇳
                    </Typography>

                </Box>

                <Typography
                    variant="h5"
                    className="title"
                >
                    Army Asset Lifecycle
                </Typography>

                <Typography className="subtitle">
                    Secure Military Asset Management
                </Typography>

                <TextField
                    fullWidth
                    label="Army Number"
                    margin="normal"
                    value={armyNumber}
                    onChange={(e) => setArmyNumber(e.target.value)}
                />

                <TextField
                    fullWidth
                    label="Password"
                    type="password"
                    margin="normal"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                {
                    error && (
                        <Alert severity="error" sx={{ mt: 2 }}>
                            {error}
                        </Alert>
                    )
                }

                <Button
                    variant="contained"
                    fullWidth
                    className="login-btn"
                    onClick={handleLogin}
                    disabled={loading}
                    sx={{ mt: 2 }}
                >
                    {
                        loading
                            ? <CircularProgress size={24} color="inherit" />
                            : "SIGN IN"
                    }
                </Button>

                <Typography
                    className="footer-text"
                    sx={{ mt: 2 }}
                >
                    Authorized Personnel Only
                </Typography>

            </Paper>

        </Box>

    );

}

export default Login;