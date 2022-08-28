import axios from 'axios';
import { url } from '../../constants';

export class EventRepository {
    token: string;

    constructor(token: string) {
        this.token = token;
    }

    getAllEvents = async () => {
        try {
            const response = await axios({
                method: 'GET',
                url: url + '/api/events/',
                headers: {
                    Authorization: 'Token ' + this.token,
                },
            });

            if (response.status === 200) {
                return response.data;
            }
            return [];
        } catch (e) {
            return [];
        }
    };
}
