import { ClearFiltersButton } from './ClearFiltersButton';
import { FilterInputs } from './FilterInputs';

export const DesktopFilters = () => {
    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                margin: '4px',
            }}>
            <ClearFiltersButton />
            <FilterInputs />
        </div>
    );
};
