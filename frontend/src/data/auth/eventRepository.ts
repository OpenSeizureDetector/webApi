import axios from 'axios';
import { url } from '../../constants';
import { getAlarmState } from '../../types/AlarmState';
import { Event } from '../../types/Event';

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
                return response.data.map((dataPoint: Event) => {
                    return {
                        ...dataPoint,
                        date: new Date(dataPoint.dataTime),
                        alarmState: getAlarmState(dataPoint.osdAlarmState),
                    };
                });
            }
            return [];
        } catch (e) {
            return [];
        }
    };
}
