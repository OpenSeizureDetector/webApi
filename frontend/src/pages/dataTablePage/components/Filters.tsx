import { SelectChangeEvent, TextField } from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers';
import { useData } from '../../../hooks/useData';
import { AlarmState } from '../../../types/AlarmState';
import { MultiSelectDropdown } from '../../../common/MultiSelectDropdown';
import { ChangeEvent } from 'react';

export const Filters = () => {
    const { filters, setFilters, eventTypes } = useData();

    const handleAlarmState = (event: SelectChangeEvent<string[]>) => {
        setFilters({
            ...filters,
            alarmState: event.target.value as AlarmState[],
        });
    };

    const handleEventType = (event: SelectChangeEvent<string[]>) => {
        setFilters({
            ...filters,
            eventType: event.target.value as string[],
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

    const handleUserId = (event: ChangeEvent<HTMLInputElement>) => {
        setFilters({
            ...filters,
            userId: event.target.value ? Number(event.target.value) : undefined,
        });
    };

    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                marginLeft: '4px',
                marginRight: '4px',
            }}>
            <MultiSelectDropdown
                label="Alarm State"
                options={Object.values(AlarmState)}
                selected={filters.alarmState}
                handleChange={handleAlarmState}
            />
            <MultiSelectDropdown
                label="Event Type"
                options={Object.keys(eventTypes)}
                selected={filters.eventType}
                handleChange={handleEventType}
            />
            <DateTimePicker
                label="Start Date"
                value={filters.startDate || null}
                onChange={handleStartDate}
                renderInput={(params) => (
                    <TextField {...params} size="small" sx={{ margin: '8px', width: 190 }} />
                )}
                ampm={false}
            />
            <DateTimePicker
                label="End Date"
                value={filters.endDate || null}
                onChange={handleEndDate}
                renderInput={(params) => (
                    <TextField {...params} size="small" sx={{ margin: '8px', width: 190 }} />
                )}
                ampm={false}
            />
            <TextField
                label="User ID"
                type="number"
                value={filters.userId}
                onChange={handleUserId}
                size="small"
                sx={{ margin: '8px', width: 100 }}
            />
        </div>
    );
};
