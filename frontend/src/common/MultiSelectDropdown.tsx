import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';

export const MultiSelectDropdown = (props: MultiSelectDropdownProps) => {
    return (
        <div>
            <FormControl sx={{ m: 1, width: 300 }}>
                <InputLabel>{props.label}</InputLabel>
                <Select
                    multiple
                    value={props.selected}
                    onChange={props.handleChange}
                    input={<OutlinedInput label={props.label} />}
                    renderValue={(selected: string[]) => selected.join(', ')}>
                    {props.options.map((option) => (
                        <MenuItem key={option} value={option}>
                            <Checkbox checked={props.selected.indexOf(option) > -1} />
                            <ListItemText primary={option} />
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
