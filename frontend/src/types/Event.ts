import { AlarmState } from './AlarmState';
import { EventType } from './EventType';

export interface Event {
    id: number;
    osdAlarmState: number;
    alarmState: AlarmState;
    dataTime: string;
    date: Date;
    desc: string;
    type: EventType;
    subType: string;
    userId: number;
}
