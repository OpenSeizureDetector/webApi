import { Box, CircularProgress, Typography } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { OSDAppBar } from '../common/AppBar';
import { Filters } from '../common/Filters';
import { renderCellExpand } from '../common/GridCellExpand';
import { useData } from '../hooks/useData';

export const Home = () => {
    const { data, isLoading } = useData();

    const columns: GridColDef[] = [
        { field: 'id', headerName: 'ID' },
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
                <div style={{ height: 'calc(100vh - 136px)', width: '100%' }}>
                    <Filters />
                    <DataGrid
                        rows={data}
                        columns={columns}
                        pageSize={50}
                        rowsPerPageOptions={[50]}
                        disableColumnFilter
                        disableSelectionOnClick
                        disableColumnMenu
                    />
                </div>
            )}
        </Box>
    );
};
