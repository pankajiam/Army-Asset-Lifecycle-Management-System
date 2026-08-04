import { Card, CardContent, Typography, Box } from "@mui/material";

function StatCard({
    title,
    value,
    icon,
    color
}) {
    return (
        <Card
            elevation={4}
            sx={{
                borderLeft: `6px solid ${color}`,
                borderRadius: 3,
                height: "100%",
            }}
        >
            <CardContent>

                <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                >

                    <Box>

                        <Typography
                            color="text.secondary"
                            variant="body2"
                        >
                            {title}
                        </Typography>

                        <Typography
                            variant="h4"
                            fontWeight="bold"
                            sx={{ mt: 1 }}
                        >
                            {value}
                        </Typography>

                    </Box>

                    <Box
                        sx={{
                            fontSize: 40,
                            color: color,
                        }}
                    >
                        {icon}
                    </Box>

                </Box>

            </CardContent>
        </Card>
    );
}

export default StatCard;