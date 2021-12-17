import { useSetRecoilState } from "recoil"
import { authState } from "../state/authState"

export const Home = () => {
    const setAuthState = useSetRecoilState(authState);
    const logout = () => setAuthState(false);
    return(<button onClick={logout}>Logout</button>)
}