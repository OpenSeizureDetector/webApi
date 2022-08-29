import { ThemeProvider } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import './App.css';
import { AuthStateProvider } from './context/AuthStateContext';
import { EventDataProvider } from './context/EventDataContext';
import { Router } from './router/Router';
import { theme } from './theme/theme';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthStateProvider>
                <EventDataProvider>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <div className="App">
                            <Router />
                        </div>
                    </LocalizationProvider>
                </EventDataProvider>
            </AuthStateProvider>
        </ThemeProvider>
    );
}

export default App;
