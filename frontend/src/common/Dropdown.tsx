import {
    FormControl,
    InputLabel,
    ListItemText,
    MenuItem,
    OutlinedInput,
    Select,
    SelectChangeEvent,
} from '@mui/material';

export const Dropdown = (props: DropdownProps) => {
    return (
        <div>
            <FormControl sx={{ m: 1, width: 300 }}>
                <InputLabel>{props.label}</InputLabel>
                <Select
                    value={props.selected}
                    onChange={props.handleChange}
                    input={<OutlinedInput label={props.label} />}>
                    {props.options.map((option) => (
                        <MenuItem key={option} value={option}>
                            <ListItemText primary={option} />
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
};

interface DropdownProps {
    options: string[];
    label: string;
    selected: string;
    handleChange: (event: SelectChangeEvent<string>) => void;
}
