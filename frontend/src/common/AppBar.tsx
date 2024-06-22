import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useAuth } from '../hooks/useAuth';

export const OSDAppBar = () => {
    const { logout } = useAuth();

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar
                    variant="dense"
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                    }}
                >
                    <div style={{ display: 'flex' }}>
                        <img src="/logo.png" height={36} />
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{ flexGrow: 1, marginLeft: 1 }}
                        >
                            OpenSeizureDetector
                        </Typography>
                    </div>
                    <Button color="inherit" onClick={logout}>
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>
        </Box>
    );
};
