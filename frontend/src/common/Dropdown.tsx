import {
    FormControl,
    InputLabel,
    ListItemText,
    MenuItem,
    OutlinedInput,
    Select,
    SelectChangeEvent,
    Typography,
} from '@mui/material';

export const Dropdown = (props: DropdownProps) => {
    return (
        <div>
            <FormControl sx={{ m: 1, width: 300 }} size="small">
                <InputLabel>{props.label}</InputLabel>
                <Select
                    value={props.selected}
                    onChange={props.handleChange}
                    renderValue={(value) => <Typography>{value}</Typography>}
                    size="small"
                    input={<OutlinedInput label={props.label} />}
                >
                    {props.options.map((option) => (
                        <MenuItem key={option} value={option} dense>
                            <ListItemText primary={option} sx={{ fontSize: 8 }} />
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
