import FilterListIcon from '@mui/icons-material/FilterList';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { useState } from 'react';
import { ClearFiltersButton } from './ClearFiltersButton';
import { FilterInputs } from './FilterInputs';

export const MobileFilters = () => {
    const [open, setOpen] = useState(false);

    const openDialogue = () => setOpen(true);
    const closeDialogue = () => setOpen(false);

    return (
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button
                variant="outlined"
                startIcon={<FilterListIcon />}
                sx={{ m: 1 }}
                onClick={openDialogue}>
                Filter
            </Button>
            {open && (
                <Dialog open={open} onClose={closeDialogue}>
                    <DialogTitle>Filter Data</DialogTitle>
                    <DialogContent>
                        <FilterInputs />
                    </DialogContent>
                    <DialogActions>
                        <ClearFiltersButton />
                        <Button onClick={closeDialogue}>Close</Button>
                    </DialogActions>
                </Dialog>
            )}
        </div>
    );
};
