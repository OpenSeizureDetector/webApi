export enum AlarmState {
    OK = 'OK',
    WARNING = 'Warning',
    ALARM = 'Alarm',
    MANUAL_ALARM = 'Manual Alarm',
    FALL = 'Fall',
}

export const getAlarmState = (state: number) => {
    switch (state) {
        case 0:
            return AlarmState.OK;
        case 1:
            return AlarmState.WARNING;
        case 2:
            return AlarmState.ALARM;
        case 3:
            return AlarmState.FALL;
        case 5:
            return AlarmState.MANUAL_ALARM;
    }
};
