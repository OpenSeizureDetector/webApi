import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    TextField,
} from '@mui/material';
import { Dropdown } from '../../common/Dropdown';
import { useData } from '../../hooks/useData';
import { Event } from '../../types/Event';

export const EditEventDialogue = (props: EditDataDialogueProps) => {
    const { eventTypes } = useData();

    return (
        <Dialog open={props.open} onClose={props.onCancel}>
            <DialogTitle>Edit Event</DialogTitle>
            <DialogContent>
                <Dropdown
                    options={Object.keys(eventTypes)}
                    label={'Event Type'}
                    selected={props.eventData.type}
                    handleChange={(event) =>
                        props.updateEvent({
                            ...props.eventData,
                            type: event.target.value,
                            subType: '',
                        })
                    }
                />
                <Dropdown
                    options={eventTypes[props.eventData.type]}
                    label={'Event Sub-Type'}
                    selected={props.eventData.subType || ''}
                    handleChange={(event) =>
                        props.updateEvent({
                            ...props.eventData,
                            subType: event.target.value,
                        })
                    }
                />
                <TextField
                    label="Notes about event"
                    value={props.eventData.desc}
                    onChange={(event) => {
                        props.updateEvent({
                            ...props.eventData,
                            desc: event.target.value,
                        });
                    }}
                    sx={{ m: 1, width: 300 }}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={props.onCancel}>Cancel</Button>
                <Button onClick={props.onSubmit}>Submit</Button>
            </DialogActions>
        </Dialog>
    );
};

interface EditDataDialogueProps {
    open: boolean;
    eventData: Event;
    updateEvent: (eventData: Event) => void;
    onCancel: () => void;
    onSubmit: () => void;
}
