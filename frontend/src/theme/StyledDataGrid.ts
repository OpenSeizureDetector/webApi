import { styled } from '@mui/material/styles';
import { DataGrid } from '@mui/x-data-grid';

export const StyledDataGrid = styled(DataGrid)(({ theme }) => ({
    border: 0,
    marginLeft: 12,
    marginRight: 12,
    '& .MuiDataGrid-iconSeparator': {
        display: 'none',
    },
    '& .MuiDataGrid-columnHeader': {
        backgroundColor: theme.palette.primary.main,
        color: 'white',
    },
    '& .MuiDataGrid-columnHeaders': {
        borderRadius: 0,
    },
    '& .MuiDataGrid-cell:focus': {
        outline: 'none',
    },
    '& .odd-row': {
        backgroundColor: '#E0E0E0',
        '&:hover': {
            backgroundColor: '#E0E0E0',
        },
    },
    '& .even-row': {
        backgroundColor: '#F5F5F5',
        '&:hover': {
            backgroundColor: '#F5F5F5',
        },
    },
}));
