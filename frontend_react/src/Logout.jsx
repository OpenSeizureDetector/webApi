import Cookies from 'js-cookie'

export default function Logout() {
    Cookies.set('LoggedIn',0);
    return (
	<div>
	    <h2>
		Logout
	    </h2>
	    <a href="/">
		Home
	    </a>
	</div>
    );
    
}
