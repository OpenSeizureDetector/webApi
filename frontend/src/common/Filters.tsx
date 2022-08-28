import { MultiSelectDropdown } from './MultiSelectDropdown';

export const Filters = () => {
    return (
        <div
            style={{
                height: 72,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
            }}>
            <MultiSelectDropdown
                label="Alarm State"
                options={['OK', 'WARNING', 'ALARM', 'MANUAL ALARM', 'FALL']}
            />
        </div>
    );
};
