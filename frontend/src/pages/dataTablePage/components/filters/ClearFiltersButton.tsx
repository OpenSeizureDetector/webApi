import { Button } from '@mui/material';
import { useData } from '../../../../hooks/useData';

export const ClearFiltersButton = () => {
    const { clearFilters } = useData();

    return (
        <Button variant="text" onClick={clearFilters} color="error">
            Clear
        </Button>
    );
};
