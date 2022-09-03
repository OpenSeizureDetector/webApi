import { ThemeProvider } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AuthStateProvider } from './context/AuthStateContext';
import { EventDataProvider } from './context/EventDataContext';
import { Router } from './router/Router';
import { theme } from './theme/theme';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import locale from 'dayjs/locale/en-gb';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthStateProvider>
                <EventDataProvider>
                    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={locale}>
                        <div style={{ textAlign: 'center' }}>
                            <Router />
                            <ToastContainer hideProgressBar position="bottom-center" />
                        </div>
                    </LocalizationProvider>
                </EventDataProvider>
            </AuthStateProvider>
        </ThemeProvider>
    );
}

export default App;
