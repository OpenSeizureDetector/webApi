import { IconButton } from '@mui/material';
import { GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { renderCellExpand } from './GridCellExpand';
import { getAlarmState } from '../../../types/AlarmState';
import EditIcon from '@mui/icons-material/Edit';

export const getGridColumns = (
    onClickEdit: (params: GridRenderCellParams) => void
): GridColDef[] => [
    { field: 'id', headerName: 'ID', sortable: false, width: 60 },
    {
        field: 'date',
        headerName: 'Date',
        valueFormatter: (params) => params.value.toLocaleString(),
        minWidth: 170,
        flex: 1,
        sortable: false,
    },
    {
        field: 'osdAlarmState',
        headerName: 'Alarm State',
        valueFormatter: (params) => getAlarmState(params.value),
        minWidth: 120,
        flex: 1,
        sortable: false,
    },
    {
        field: 'type',
        headerName: 'Type',
        minWidth: 120,
        flex: 1,
        sortable: false,
    },
    {
        field: 'subType',
        headerName: 'Sub Type',
        minWidth: 250,
        flex: 1,
        sortable: false,
    },
    {
        field: 'desc',
        headerName: 'Description',
        flex: 5,
        minWidth: 230,
        sortable: false,
        renderCell: renderCellExpand,
    },
    { field: 'userId', headerName: 'User ID', sortable: false, width: 75 },
    {
        field: 'edit',
        headerName: '',
        sortable: false,
        renderCell: (params: GridRenderCellParams) => (
            <IconButton
                onClick={() => onClickEdit(params)}
                size="small"
                style={{ margin: 0 }}
                tabIndex={params.hasFocus ? 0 : -1}>
                <EditIcon />
            </IconButton>
        ),
        width: 34,
    },
];
