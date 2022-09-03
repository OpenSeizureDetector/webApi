import { Box, CircularProgress, Typography } from '@mui/material';
import { GridRenderCellParams } from '@mui/x-data-grid';
import { OSDAppBar } from '../../common/AppBar';
import { Filters } from './components/filters/Filters';
import { useData } from '../../hooks/useData';
import { StyledDataGrid } from '../../theme/StyledDataGrid';
import { Event } from '../../types/Event';
import { EditEventDialogue } from './components/EditEventDialogue';
import { useState } from 'react';
import { EventRepository } from '../../data/eventRepository';
import { useAuth } from '../../hooks/useAuth';
import { getGridColumns } from './components/GridColumns';

export const DataTablePage = () => {
    const { filteredData, isLoading, data, setData } = useData();
    const { token } = useAuth();

    ///////////////////////////
    // dialogue to edit data //
    ///////////////////////////

    const [open, setOpen] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);

    const openDialogue = (eventData: Event) => {
        setSelectedEvent(eventData);
        setOpen(true);
    };
    const closeDialogue = () => setOpen(false);

    const updateEvent = (eventData: Event) => setSelectedEvent(eventData);

    const saveEvent = () => {
        if (selectedEvent)
            new EventRepository(token ?? '')
                .updateEvent(selectedEvent, data, setData)
                .then(closeDialogue);
    };

    //////////////////////////

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <OSDAppBar />
            {isLoading ? (
                <div>
                    <CircularProgress sx={{ margin: '16px' }} />
                    <Typography>Loading data.... This may take some time.</Typography>
                </div>
            ) : (
                <div style={{ height: 'calc(100vh - 104px)', width: '100%' }}>
                    <Filters />
                    <StyledDataGrid
                        rows={filteredData}
                        columns={getGridColumns((params: GridRenderCellParams) =>
                            openDialogue(params.row)
                        )}
                        pageSize={50}
                        rowsPerPageOptions={[50]}
                        disableColumnFilter
                        disableColumnMenu
                        disableSelectionOnClick
                        getRowClassName={(params) =>
                            params.indexRelativeToCurrentPage % 2 === 0 ? 'even-row' : 'odd-row'
                        }
                        density="compact"
                    />
                    {open && selectedEvent && (
                        <EditEventDialogue
                            open={open}
                            onCancel={closeDialogue}
                            onSubmit={saveEvent}
                            eventData={selectedEvent}
                            updateEvent={updateEvent}
                        />
                    )}
                </div>
            )}
        </Box>
    );
};
