import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import { Typography } from '@mui/material';

export const MultiSelectDropdown = (props: MultiSelectDropdownProps) => {
    return (
        <div>
            <FormControl sx={{ m: 1, width: 200 }} size="small">
                <InputLabel>{props.label}</InputLabel>
                <Select
                    multiple
                    size="small"
                    value={props.selected}
                    onChange={props.handleChange}
                    input={<OutlinedInput label={props.label} />}
                    renderValue={(selected: string[]) => (
                        <Typography sx={{ textAlign: 'start' }}>{selected.join(', ')}</Typography>
                    )}>
                    {props.options.map((option) => (
                        <MenuItem key={option} value={option} dense>
                            <Checkbox size="small" checked={props.selected.indexOf(option) > -1} />
                            <ListItemText primary={option} sx={{ fontSize: 8 }} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
};

interface MultiSelectDropdownProps {
    options: string[];
    label: string;
    selected: string[];
    handleChange: (event: SelectChangeEvent<string[]>) => void;
}
