import './App.css';
import Cookies from 'js-cookie'




function App() {
    console.log("Main App LoggedIn Cookie" + Cookies.get('LoggedIn'));
    return (
	<div className="App">
	    <header className="App-header">
		<a href="/login">Login</a>
		<a href="/reset-pw">ResetPw</a>
		<a href="/profile">Edit User Profile</a>
		<a href="/register">Register</a>
		<a href="/logout">Logout</a>
	    </header>
	</div>
    );
}

export default App;
