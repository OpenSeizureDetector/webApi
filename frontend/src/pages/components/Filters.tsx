import { SelectChangeEvent, TextField, Typography } from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers';
import { useData } from '../../hooks/useData';
import { AlarmState } from '../../types/AlarmState';
import { EventType } from '../../types/EventType';
import { MultiSelectDropdown } from '../../common/MultiSelectDropdown';

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

    const handleStartDate = (value: Date | null) => {
        setFilters({
            ...filters,
            startDate: value ?? undefined,
        });
    };

    const handleEndDate = (value: Date | null) => {
        setFilters({
            ...filters,
            endDate: value ?? undefined,
        });
    };

    return (
        <div
            style={{
                height: 72,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                margin: 12,
            }}>
            <Typography variant="h6">Filters</Typography>
            <div
                style={{
                    display: 'flex',
                    alignItems: 'center',
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
                <DateTimePicker
                    label="Start Date"
                    value={filters.startDate || null}
                    onChange={handleStartDate}
                    renderInput={(params) => <TextField {...params} sx={{ margin: '8px' }} />}
                    ampm={false}
                />
                <DateTimePicker
                    label="End Date"
                    value={filters.endDate || null}
                    onChange={handleEndDate}
                    renderInput={(params) => <TextField {...params} sx={{ margin: '8px' }} />}
                    ampm={false}
                />
            </div>
        </div>
    );
};
