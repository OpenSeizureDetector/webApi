import axios from "axios";

const url = 'https://osdapi.ddns.net';

export const LoginFn = async (username:string, password:string):Promise<string | null> => {
    const response = await axios({
        method: 'POST',
        url: url + '/api/accounts/login/',
        data: {
            login: username,
            password: password
        },
        validateStatus: (status) => status < 500
    });
    if (response.status === 200) {
        return response.data['token'];
    } 
    return null;
}