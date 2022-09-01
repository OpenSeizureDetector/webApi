import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useReducer, useState } from 'react';
import { AuthRepository } from '../data/authRepository';
import { CircularProgress } from '@mui/material';
import { useAuth } from '../hooks/useAuth';

export const Login = () => {
    const [state, dispatch] = useReducer(reducer, initialState);
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();

    const handleUsernameChange: React.ChangeEventHandler<HTMLInputElement> = (event) => {
        dispatch({
            type: 'setUsername',
            payload: event.target.value,
        });
    };

    const handlePasswordChange: React.ChangeEventHandler<HTMLInputElement> = (event) => {
        dispatch({
            type: 'setPassword',
            payload: event.target.value,
        });
    };

    const handleLogin = async (event: React.FormEvent<HTMLInputElement>) => {
        event.preventDefault();
        setIsLoading(true);
        const { code, message } = await new AuthRepository().signIn(state.username, state.password);
        setIsLoading(false);
        if (code === '200' && login) {
            login(message);
        } else {
            dispatch({
                type: 'loginFailed',
                payload: 'Unable to login.  Please check your username and password.',
            });
        }
    };

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
                sx={{
                    marginTop: 4,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                <img
                    src="https://www.openseizuredetector.org.uk/wp-content/uploads/2015/02/icon_48x48.png"
                    style={{ margin: 8 }}
                />
                <Typography component="h1" variant="h5">
                    Sign in to OSD
                </Typography>
                <Box component="form" onSubmit={handleLogin}>
                    <TextField
                        error={state.hasError}
                        fullWidth
                        id="username"
                        type="text"
                        label="Username"
                        placeholder="Username"
                        margin="normal"
                        onChange={handleUsernameChange}
                        required
                        autoFocus
                        inputProps={{
                            autoComplete: 'new-password',
                            form: {
                                autoComplete: 'off',
                            },
                        }}
                    />
                    <TextField
                        error={state.hasError}
                        fullWidth
                        id="password"
                        type="password"
                        label="Password"
                        placeholder="Password"
                        margin="normal"
                        helperText={state.helperText}
                        onChange={handlePasswordChange}
                        required
                        name="password"
                        inputProps={{
                            autoComplete: 'new-password',
                            form: {
                                autoComplete: 'off',
                            },
                        }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2, height: 52 }}>
                        {isLoading ? (
                            <CircularProgress color="inherit" />
                        ) : (
                            <p style={{ margin: 0 }}>Sign In</p>
                        )}
                    </Button>
                    <Link href="/register" variant="body2">
                        {"Don't have an account? Sign Up"}
                    </Link>
                </Box>
            </Box>
        </Container>
    );
};

type State = {
    username: string;
    password: string;
    hasError: boolean;
    helperText: string;
};

const initialState: State = {
    username: '',
    password: '',
    hasError: false,
    helperText: '',
};

type Action =
    | { type: 'setUsername'; payload: string }
    | { type: 'setPassword'; payload: string }
    | { type: 'loginFailed'; payload: string }
    | { type: 'setHasError'; payload: boolean };

const reducer = (state: State, action: Action): State => {
    switch (action.type) {
        case 'setUsername':
            return {
                ...state,
                username: action.payload,
                hasError: false,
            };
        case 'setPassword':
            return {
                ...state,
                password: action.payload,
                hasError: false,
            };
        case 'loginFailed':
            return {
                ...state,
                helperText: action.payload,
                hasError: true,
            };
        case 'setHasError':
            return {
                ...state,
                hasError: action.payload,
            };
    }
};
