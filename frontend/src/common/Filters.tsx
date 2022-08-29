import { SelectChangeEvent } from '@mui/material';
import { useData } from '../hooks/useData';
import { AlarmState } from '../types/AlarmState';
import { EventType } from '../types/EventType';
import { MultiSelectDropdown } from './MultiSelectDropdown';

export const Filters = () => {
    const { filters, setFilters } = useData();

    const handleAlarmState = (event: SelectChangeEvent<string[]>) => {
        setFilters({
            ...filters,
            alarmState: event.target.value as AlarmState[],
        });
    };

    const handleEventType = (event: SelectChangeEvent<string[]>) => {
        setFilters({
            ...filters,
            eventType: event.target.value as EventType[],
        });
    };

    return (
        <div
            style={{
                height: 72,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                margin: 12,
            }}>
            <MultiSelectDropdown
                label="Alarm State"
                options={Object.values(AlarmState)}
                selected={filters.alarmState}
                handleChange={handleAlarmState}
            />
            <MultiSelectDropdown
                label="Event Type"
                options={Object.values(EventType)}
                selected={filters.eventType}
                handleChange={handleEventType}
            />
        </div>
    );
};
