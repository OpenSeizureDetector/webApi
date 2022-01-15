import React, { useReducer, useRef } from "react";
import { useStyles } from "./styles"
import { Button, Card, CardActions, CardContent, CardHeader, TextField, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { RegisterErrors, RegisterFn } from "../api/auth";

export const Register = () => {
    const classes = useStyles();
    const [state, dispatch] = useReducer(reducer, initialState);
    const navigate = useNavigate();
    const formRef = useRef<HTMLFormElement>(null);

    const handleUsernameChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setUsername',
            payload: event.target.value
        });
    }

    const handleFirstNameChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setFirstName',
            payload: event.target.value
        });
    }

    const handleLastNameChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setLastName',
            payload: event.target.value
        });
    }

    const handleEmailChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setEmail',
            payload: event.target.value
        });
    }

    const handlePasswordChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setPassword',
            payload: event.target.value
        });
    }

    const handleConfirmPasswordChange: React.ChangeEventHandler<HTMLInputElement> = event => {
        dispatch({
            type: 'setConfirmPassword',
            payload: event.target.value
        });
    }

    const handleRegister = async () => {
        formRef.current?.reportValidity();
        var errors: RegisterErrors | null;
        if (state.password !== state.confirmPassword) {
            errors = {
                username: [],
                first_name: [],
                last_name: [],
                email: [],
                password: ['Passwords do not match'],
                confirm_password: ['Passwords do not match'],
                non_field_errors: []
            };
        } else {
            errors = await RegisterFn(
                state.username,
                state.firstName,
                state.lastName,
                state.email,
                state.password,
                state.confirmPassword
            );
        }
        if (errors === null) {
            navigate('/', {replace: true});
        } else {
            dispatch({
                type: 'createUserFailed',
                payload: errors
            });
        }
    }

    return (
        <form className={classes.container} ref={formRef} autoComplete="off">
            <Card className={classes.card}>
                <CardHeader className={classes.header} title="OpenSeizureDetector Web API" />
                <CardContent>
                    <div>
                        <TextField
                            error={state.usernameHasErr}
                            helperText={state.usernameErr}
                            fullWidth
                            id="username"
                            type="text"
                            label="Username"
                            placeholder="Username"
                            margin="normal"
                            onChange={handleUsernameChange}
                            required
                        />
                        <TextField
                            error={state.firstNameHasErr}
                            helperText={state.firstNameErr}
                            fullWidth
                            id="firstname"
                            type="text"
                            label="First Name"
                            placeholder="First Name"
                            margin="normal"
                            onChange={handleFirstNameChange}
                            required
                        />
                        <TextField
                            error={state.lastNameHasErr}
                            helperText={state.lastNameErr}
                            fullWidth
                            id="lastname"
                            type="text"
                            label="Last Name"
                            placeholder="Last Name"
                            margin="normal"
                            onChange={handleLastNameChange}
                            required
                        />
                        <TextField
                            error={state.emailHasErr}
                            helperText={state.emailErr}
                            fullWidth
                            id="email"
                            type="email"
                            label="Email"
                            placeholder="Email"
                            margin="normal"
                            onChange={handleEmailChange}
                            required
                        />
                        <TextField
                            error={state.passwordHasErr}
                            helperText={state.passwordErr}
                            fullWidth
                            id="password"
                            type="password"
                            label="Password"
                            placeholder="Password"
                            margin="normal"
                            onChange={handlePasswordChange}
                            required
                        />
                        <TextField
                            error={state.confirmPasswordHasErr}
                            helperText={state.confirmPasswordErr}
                            fullWidth
                            id="confirmpassword"
                            type="password"
                            label="Confirm Password"
                            placeholder="Confirm Password"
                            margin="normal"
                            onChange={handleConfirmPasswordChange}
                            required
                        />
                        <div className={classes.spacer16} />
                        <Typography color='#D74545'>{state.helperText}</Typography>
                    </div>
                </CardContent>
                <CardActions className={classes.actions}>
                    <Button
                        variant="contained"
                        size="large"
                        color="secondary"
                        className={classes.loginBtn}
                        onClick={handleRegister}
                    >
                        Create Account
                    </Button>
                </CardActions>
                <CardContent>
                    <div className={classes.row}>
                        <Typography className={classes.minimiseWidth}>Already have an account?</Typography>
                        <Link to="/">
                            <Button
                                color="info"
                            >Sign in</Button>
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </form>
    )
}

type State = {
    username: string
    firstName: string
    lastName: string
    email: string
    password: string
    confirmPassword: string
    helperText: string,
    usernameHasErr: boolean,
    usernameErr: string,
    firstNameHasErr: boolean,
    firstNameErr: string,
    lastNameHasErr: boolean,
    lastNameErr: string,
    emailHasErr: boolean,
    emailErr: string,
    passwordHasErr: boolean,
    passwordErr: string,
    confirmPasswordHasErr: boolean,
    confirmPasswordErr: string
}

const initialState: State = {
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    helperText: '',
    usernameHasErr: false,
    usernameErr: '',
    firstNameHasErr: false,
    firstNameErr: '',
    lastNameHasErr: false,
    lastNameErr: '',
    emailHasErr: false,
    emailErr: '',
    passwordHasErr: false,
    passwordErr: '',
    confirmPasswordHasErr: false,
    confirmPasswordErr: ''
}

type Action =
    { type: 'setUsername', payload: string } |
    { type: 'setFirstName', payload: string } |
    { type: 'setLastName', payload: string } |
    { type: 'setEmail', payload: string } |
    { type: 'setPassword', payload: string } |
    { type: 'setConfirmPassword', payload: string } |
    { type: 'createUserFailed', payload: RegisterErrors }


const reducer = (state: State, action: Action): State => {
    switch (action.type) {
        case 'setUsername':
            return {
                ...state,
                username: action.payload
            }
        case 'setFirstName':
            return {
                ...state,
                firstName: action.payload
            }
        case 'setLastName':
            return {
                ...state,
                lastName: action.payload
            }
        case 'setEmail':
            return {
                ...state,
                email: action.payload
            }
        case 'setPassword':
            return {
                ...state,
                password: action.payload
            }
        case 'setConfirmPassword':
            return {
                ...state,
                confirmPassword: action.payload
            }
        case 'createUserFailed':
            return {
                ...state,
                usernameErr: action.payload.username && action.payload.username.length ? action.payload.username[0] : '',
                usernameHasErr: action.payload.username && action.payload.username.length ? true : false,
                firstNameErr: action.payload.first_name && action.payload.first_name.length ? action.payload.first_name[0] : '',
                firstNameHasErr: action.payload.first_name && action.payload.first_name.length ? true : false,
                lastNameErr: action.payload.last_name && action.payload.last_name.length ? action.payload.last_name[0] : '',
                lastNameHasErr: action.payload.last_name && action.payload.last_name.length ? true : false,
                emailErr: action.payload.email && action.payload.email.length ? action.payload.email[0] : '',
                emailHasErr: action.payload.email && action.payload.email.length ? true : false,
                passwordErr: action.payload.password && action.payload.password.length ? action.payload.password[0] : '',
                passwordHasErr: action.payload.password && action.payload.password.length ? true : false,
                confirmPasswordErr: action.payload.confirm_password && action.payload.confirm_password.length ? action.payload.confirm_password[0] : '',
                confirmPasswordHasErr: action.payload.confirm_password && action.payload.confirm_password.length ? true : false,
                helperText: action.payload.non_field_errors && action.payload.non_field_errors.length ? action.payload.non_field_errors[0] : 'Unable to create account',
            }
    }
}