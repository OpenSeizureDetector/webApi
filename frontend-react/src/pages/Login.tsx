import { Button, Card, CardActions, CardContent, CardHeader, TextField, Typography } from "@mui/material";
import { useReducer } from "react";
import { useSetRecoilState } from "recoil";
import { LoginFn } from "../api/auth";
import { authState, tokenState } from "../state/authState";
import { useStyles } from "./styles";

export const Login = () => {
    const classes = useStyles();
    const [state, dispatch] = useReducer(reducer, initialState);
    const setAuthState = useSetRecoilState(authState);
    const setToken = useSetRecoilState(tokenState);

    const handleUsernameChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setUsername',
            payload: event.target.value
        });
    }

    const handlePasswordChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setPassword',
            payload: event.target.value
        });
    }

    const handleLogin = async () => {
        let token = await LoginFn(state.username, state.password);
        if (token) {
            setAuthState(true);
            setToken(token);
        } else {
            dispatch({
                type: 'loginFailed',
                payload: 'Incorrect username or password'
            });
        }
    }

    return(
        <form className={classes.container} autoComplete="off">
            <Card className={classes.card}>
                <CardHeader className={classes.header} title="OpenSeizureDetector Web API" />
                <CardContent>
                    <div>
                        <TextField
                            error={state.hasError}
                            fullWidth
                            id="username"
                            type="email"
                            label="Username"
                            placeholder="Username"
                            margin="normal"
                            onChange={handleUsernameChange}
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
                        />
                    </div>
                </CardContent>
                <CardActions className={classes.actions}>
                    <Button
                        variant="contained"
                        size="large"
                        color="secondary"
                        className={classes.loginBtn}
                        onClick={handleLogin} >
                        Login
                    </Button>
                </CardActions>
                <CardContent>
                    <div className={classes.row}>
                        <Typography className={classes.minimiseWidth}>Forgotten your password?</Typography>
                        <Button
                            color="info"
                        >Reset Password</Button>
                    </div>
                    <div className={classes.row}>
                        <Typography className={classes.minimiseWidth}>New user?</Typography>
                        <Button
                            color="info"
                        >Create Account</Button>
                    </div>
                </CardContent>
            </Card>
        </form>
    )
}

type State = {
    username: string
    password: string
    hasError: boolean
    helperText: string
}

const initialState:State = {
    username: '',
    password: '',
    hasError: false,
    helperText: ''
}

type Action = 
    { type: 'setUsername', payload: string } |
    { type: 'setPassword', payload: string } |
    { type: 'loginFailed', payload: string } |
    { type: 'setHasError', payload: boolean }

const reducer = (state: State, action: Action): State => {
    switch (action.type) {
        case 'setUsername':
            return {
                ...state,
                username: action.payload
            }
        case 'setPassword':
            return {
                ...state,
                password: action.payload
            }
        case 'loginFailed':
            return {
                ...state,
                helperText: action.payload,
                hasError: true
            }
        case 'setHasError':
            return {
                ...state,
                hasError: action.payload
            }
    }
}