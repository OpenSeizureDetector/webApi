import { Button, Card, CardActions, CardContent, CardHeader, TextField, Typography } from "@mui/material";
import { useReducer } from "react";
import { useSetRecoilState } from "recoil"
import { authState } from "../state/auth"
import { useStyles } from "./styles";

export const Login = () => {
    const classes = useStyles();
    const [state, dispatch] = useReducer(reducer, initialState);

    const setAuthState = useSetRecoilState(authState);
    const login = () => setAuthState(true);
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
                        />
                    </div>
                </CardContent>
                <CardActions className={classes.actions}>
                    <Button
                        variant="contained"
                        size="large"
                        color="secondary"
                        className={classes.loginBtn}
                        onClick={login} >
                        Login
                    </Button>
                </CardActions>
                <CardContent>
                    <div className={classes.alignRight}>
                        <Typography className={classes.minimiseWidth}>Forgotten your password?</Typography>
                    </div>
                    <Typography>New user?</Typography>
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