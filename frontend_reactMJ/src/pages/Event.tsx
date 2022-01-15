import { Button, Card, CardActions, CardContent, CardHeader, TextField, Typography } from "@mui/material";
import { useReducer } from "react";
import { Link } from "react-router-dom";
//import { LoginFn } from "../api/auth";
import { useRecoilState } from "recoil";
import { authState, tokenState } from "../state/authState";
import { useStyles } from "./styles";
import "../App.css";

export const Event = () => {
    console.log("Event()");
    const classes = useStyles();
    const [state, ] = useReducer(reducer, initialState);
    const [authValue,] = useRecoilState(authState);
    const [tokenValue,] = useRecoilState(tokenState);
    console.log("tokenValue="+tokenValue);

    const handleSave = async () => {
        //let token = await LoginFn(state.username, state.password);
        
    }

    if (authValue)
      return (
            <form className={classes.container} autoComplete="off">
            <Card className={classes.card}>
                <CardHeader className={classes.header} title="OpenSeizureDetector: Edit Event" />
                <CardContent>
                    <div>
    		    
                        <TextField
                            error={state.hasError}
                            fullWidth
                            id="desc"
                            type="text"
                            label="Description"
                            placeholder="Event Description"
                            margin="normal"
                        />
                    </div>
                </CardContent>
                <CardActions className={classes.actions}>
                    <Button
                        variant="contained"
                        size="large"
                        color="secondary"
                        className={classes.loginBtn}
                        onClick={handleSave} >
                        Save
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
                        <Link to="register">
                            <Button
                                color="info"
                            >Create Account</Button>
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </form>
	);    

    return (
    <div>
<h1> Not Logged In</h1>
       <a href="../Login">Login</a>
       </div>
       );

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