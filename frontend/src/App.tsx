import { ThemeProvider } from '@mui/material';
import './App.css';
import { AuthStateProvider } from './context/AuthStateContext';
import { EventDataProvider } from './context/EventDataContext';
import { Router } from './router/Router';
import { theme } from './theme/theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthStateProvider>
                <EventDataProvider>
                    <div className="App">
                        <Router />
                    </div>
                </EventDataProvider>
            </AuthStateProvider>
        </ThemeProvider>
    );
}

export default App;
