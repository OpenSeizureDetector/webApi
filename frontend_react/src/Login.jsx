import Cookies from 'js-cookie'
import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


export default function Login() {
    const [uname, setUname] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    function validateForm() {
	return uname.length > 0 && password.length > 0;
    }

    function handleSubmit(event) {
	window.alert("handleSubmit");
	console.log("Login.handlesubmit - uname="+uname+" pwd="+password);
	event.preventDefault();
	//getState();

	axios(
	    {
		method: 'post',
		url: 'https://osdapi.ddns.net/api/accounts/login/',
		data: {
		    login: uname,
		    password: password,
		},
		validateStatus: function(status) {
		    return status<500;
		},
	    }
	)
	    .then(response => {
		if (response.status === 200) {
		    console.log(response.status +
				" - " + response.statusText +
				" : " +JSON.stringify(response.data));
                    Cookies.set('token',response.data['token']);
                    Cookies.set('LoggedIn',1);
		    
		    
		    console.log("redirecting to home page");
		    navigate('/');
		} else {
		    console.log(response.status +
				" - " + response.statusText +
				" : " +JSON.stringify(response.data));
		    alert(JSON.stringify(response.data));
                    Cookies.set('token',null);
                    Cookies.set('LoggedIn',0);
		}
	    })
	    .catch((err) => {
		console.log("catch(): err="+JSON.stringify(err));
		alert(JSON.stringify(err));
                Cookies.set('token',null);
                Cookies.set('LoggedIn',0);
	    });
    }
    
    
	
	


    Cookies.set('LoggedIn',1);
    console.log("LoggedIn Cookie="+Cookies.get('LoggedIn'));
    return (   
	<div className="Login">
	    <Form onSubmit={handleSubmit}>
		<Form.Group size="lg" controlId="uname">
		    <Form.Label>User Name</Form.Label>
		    <Form.Control
			type="text"
			value={uname}
			onChange={(e) => setUname(e.target.value)}
		    />
		</Form.Group>
		<Form.Group size="lg" controlId="password">
		    <Form.Label>Password</Form.Label>
		    <Form.Control
			type="password"
			value={password}
			onChange={(e) => setPassword(e.target.value)}
		    />
		</Form.Group>
		<Button block size="lg" type="submit" disabled={!validateForm()}>
		    Login
		</Button>
	    </Form>
	    <a href="/">Home</a>
	</div>
    );
    
}
