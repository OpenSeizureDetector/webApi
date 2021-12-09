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

export const RegisterFn = async (
    username:string,
    firstName:string,
    lastName:string,
    email:string,
    password:string,
    confirmPassword:string
):Promise<RegisterErrors | null> => {
    const response = await axios({
        method: 'POST',
        url: url + '/api/accounts/register/',
        data: {
            username: username,
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            password_confirm: confirmPassword
        },
        validateStatus: (status) => status < 500
    });
    if (response.status === 201) {
        return null;
    }
    let errors:RegisterErrors = {
        username: response.data['username'],
        first_name: response.data['first_name'],
        last_name: response.data['last_name'],
        email: response.data['email'],
        password: response.data['password'],
        confirm_password: response.data['confirm_password'],
        non_field_errors: response.data['non_field_errors']
    }
    return errors;
}

export type RegisterErrors = {
    username: string[] | null
    first_name: string[] | null
    last_name: string[] | null
    email: string[] | null
    password: string[] | null
    confirm_password: string[] | null
    non_field_errors: string[] | null    
}

