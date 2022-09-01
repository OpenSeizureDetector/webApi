import * as React from 'react';
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
                <Toolbar variant="dense">
                    <img
                        src="https://www.openseizuredetector.org.uk/wp-content/uploads/2015/02/icon_48x48.png"
                        height={36}
                    />
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        OpenSeizureDetector
                    </Typography>
                    <Button color="inherit" onClick={logout}>
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>
        </Box>
    );
};
