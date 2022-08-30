import { Box, Button, CircularProgress, Typography } from '@mui/material';
import { GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { OSDAppBar } from '../common/AppBar';
import { Filters } from './components/Filters';
import { renderCellExpand } from '../common/GridCellExpand';
import { useData } from '../hooks/useData';
import { StyledDataGrid } from '../theme/StyledDataGrid';
import { Event } from '../types/Event';
import { EditEventDialogue } from './components/EditEventDialogue';
import { useState } from 'react';
import { EventRepository } from '../data/auth/eventRepository';
import { useAuth } from '../hooks/useAuth';

export const Home = () => {
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

    const columns: GridColDef[] = [
        { field: 'id', headerName: 'ID', sortable: false, headerClassName: 'table-header' },
        {
            field: 'date',
            headerName: 'Date',
            valueFormatter: (params) => params.value.toLocaleString(),
            width: 200,
            sortable: false,
        },
        {
            field: 'osdAlarmState',
            headerName: 'Alarm State',
            valueFormatter: (params) => {
                switch (params.value) {
                    case 1:
                        return 'OK';
                    case 2:
                        return 'WARNING';
                    case 3:
                        return 'ALARM';
                    case 4:
                        return 'MANUAL ALARM';
                    case 5:
                        return 'FALL';
                    default:
                        return 'UNKNOWN';
                }
            },
            width: 200,
            sortable: false,
        },
        {
            field: 'type',
            headerName: 'Type',
            width: 200,
            sortable: false,
        },
        {
            field: 'subType',
            headerName: 'Sub Type',
            width: 300,
            sortable: false,
        },
        {
            field: 'desc',
            headerName: 'Description',
            flex: 1,
            sortable: false,
            renderCell: renderCellExpand,
        },
        { field: 'userId', headerName: 'User ID', sortable: false },
        {
            field: 'edit',
            headerName: '',
            sortable: false,
            renderCell: (params: GridRenderCellParams) => (
                <strong>
                    <Button
                        onClick={() => openDialogue(params.row)}
                        variant="contained"
                        size="small"
                        style={{ margin: 0 }}
                        tabIndex={params.hasFocus ? 0 : -1}>
                        Edit
                    </Button>
                </strong>
            ),
        },
    ];

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <OSDAppBar />
            {isLoading ? (
                <div>
                    <CircularProgress sx={{ margin: '16px' }} />
                    <Typography>Loading data.... This may take some time.</Typography>
                </div>
            ) : (
                <div style={{ height: 'calc(100vh - 160px)', width: '100%' }}>
                    <Filters />
                    <StyledDataGrid
                        rows={filteredData}
                        columns={columns}
                        pageSize={50}
                        rowsPerPageOptions={[50]}
                        disableColumnFilter
                        disableColumnMenu
                        disableSelectionOnClick
                        getRowClassName={(params) =>
                            params.indexRelativeToCurrentPage % 2 === 0 ? 'even-row' : 'odd-row'
                        }
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
