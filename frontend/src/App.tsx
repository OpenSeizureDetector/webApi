import { ThemeProvider } from '@mui/material';
import './App.css';
import { AuthStateProvider } from './context/AuthStateContext';
import { Router } from './router/Router';
import { theme } from './theme/theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthStateProvider>
                <div className="App">
                    <Router />
                </div>
            </AuthStateProvider>
        </ThemeProvider>
    );
}

export default App;
