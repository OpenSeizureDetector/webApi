import { AlarmState } from './AlarmState';
import { EventType } from './EventType';

export interface Filters {
    alarmState: AlarmState[];
    eventType: EventType[];
}
