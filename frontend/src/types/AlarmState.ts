export enum AlarmState {
    OK = 'OK',
    WARNING = 'WARNING',
    ALARM = 'ALARM',
    MANUAL_ALARM = 'MANUAL ALARM',
    FALL = 'FALL',
}

export const getAlarmState = (state: number) => {
    switch (state) {
        case 1:
            return AlarmState.OK;
        case 2:
            return AlarmState.WARNING;
        case 3:
            return AlarmState.ALARM;
        case 4:
            return AlarmState.MANUAL_ALARM;
        case 5:
            return AlarmState.FALL;
    }
};
