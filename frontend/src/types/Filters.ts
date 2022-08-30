import { AlarmState } from './AlarmState';

export interface Filters {
    alarmState: AlarmState[];
    eventType: string[];
    startDate?: Date;
    endDate?: Date;
}
