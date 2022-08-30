import { AlarmState } from './AlarmState';

export interface Event {
    id: number;
    osdAlarmState: number;
    alarmState: AlarmState;
    dataTime: string;
    date: Date;
    desc: string;
    type: string;
    subType: string;
    userId: number;
}
