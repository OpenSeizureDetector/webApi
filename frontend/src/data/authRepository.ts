import axios from 'axios';
import { url } from '../constants';

export class AuthRepository {
    signIn = async (username: string, password: string): Promise<Response> => {
        try {
            const response = await axios({
                method: 'POST',
                url: url + '/api/accounts/login/',
                data: {
                    login: username,
                    password: password,
                },
                validateStatus: (status) => status < 500,
            });
            if (response.status === 200) {
                return {
                    code: '200',
                    message: response.data['token'],
                };
            }
            return {
                code: '500',
                message: 'Incorrect username or password',
            };
        } catch (e) {
            if (axios.isAxiosError(e)) {
                return {
                    code: e.code ?? '400',
                    message: e.message,
                };
            }
            return {
                code: '500',
                message: 'Unable to sign in',
            };
        }
    };

    signUp = async (
        username: string,
        firstName: string,
        lastName: string,
        email: string,
        password: string,
        confirmPassword: string
    ): Promise<RegisterErrors | null> => {
        try {
            const response = await axios({
                method: 'POST',
                url: url + '/api/accounts/register/',
                data: {
                    username: username,
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password,
                    password_confirm: confirmPassword,
                },
                validateStatus: (status) => status < 500,
            });

            if (response.status === 201) return null;

            return {
                username: response.data['username'],
                first_name: response.data['first_name'],
                last_name: response.data['last_name'],
                email: response.data['email'],
                password: response.data['password'],
                confirm_password: response.data['confirm_password'],
                non_field_errors: response.data['non_field_errors'],
            };
        } catch (error) {
            return {
                username: null,
                first_name: null,
                last_name: null,
                email: null,
                password: null,
                confirm_password: null,
                non_field_errors: ['Unable to register user. Please try again.'],
            };
        }
    };
}

interface Response {
    code: string;
    message: string;
}

export type RegisterErrors = {
    username: string[] | null;
    first_name: string[] | null;
    last_name: string[] | null;
    email: string[] | null;
    password: string[] | null;
    confirm_password: string[] | null;
    non_field_errors: string[] | null;
};
