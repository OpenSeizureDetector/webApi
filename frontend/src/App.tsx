import { ThemeProvider } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers';
import './App.css';
import { AuthStateProvider } from './context/AuthStateContext';
import { EventDataProvider } from './context/EventDataContext';
import { Router } from './router/Router';
import { theme } from './theme/theme';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import locale from 'dayjs/locale/en-gb';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthStateProvider>
                <EventDataProvider>
                    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={locale}>
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
