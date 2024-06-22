import { ClearFiltersButton } from './ClearFiltersButton';
import { FilterInputs } from './FilterInputs';

export const DesktopFilters = () => {
    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                marginLeft: '4px',
                marginRight: '4px',
            }}
        >
            <ClearFiltersButton />
            <FilterInputs />
        </div>
    );
};
