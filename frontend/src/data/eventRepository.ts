import axios from 'axios';
import { toast } from 'react-toastify';
import { url } from '../constants';
import { getAlarmState } from '../types/AlarmState';
import { Event } from '../types/Event';

export class EventRepository {
    token: string;

    constructor(token: string) {
        this.token = token;
    }

    getEventTypes = async () => {
        try {
            const response = await axios({
                method: 'GET',
                url: url + '/static/eventTypes.json',
                headers: {
                    Authorization: 'Token ' + this.token,
                },
            });

            if (response.status === 200) {
                return response.data;
            }
            return fallbackEventTypes;
        } catch (e) {
            return fallbackEventTypes;
        }
    };

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
                        type: dataPoint.type || 'Unknown',
                    };
                });
            }

            toast.error('Unable to fetch data');
            return [];
        } catch (e) {
            toast.error('Unable to fetch data');
            return [];
        }
    };

    updateEvent = async (eventData: Event, events: Event[], setData: (data: Event[]) => void) => {
        try {
            await axios({
                method: 'PUT',
                url: url + '/api/events/' + eventData.id + '/',
                headers: {
                    Authorization: 'Token ' + this.token,
                },
                data: eventData,
            });
            setData(events.map((event) => (event.id === eventData.id ? eventData : event)));
        } catch (e) {
            toast.error('Unable to update event');
        }
    };
}

const fallbackEventTypes = {
    Seizure: ['Tonic-Clonic', 'Aura', 'Other'],
    Fall: ['Stumble', 'Controlled', 'Uncontrolled'],
    'Other Medical Issue': ['Fever', 'Cold', 'Other'],
    'False Alarm': [
        'Brushing Teeth',
        'Brushing Hair',
        'Computer Games',
        'Cycling',
        'Knitting',
        'Motor Vehicle',
        'Mowing Lawn',
        'Pushing Pram/Wheelchair',
        'Sorting',
        'Talking',
        'Typing',
        'Washing / cleaning',
        'Other (Please describe in notes)',
        'Unknown',
    ],
    Unknown: ['Unknown'],
};
