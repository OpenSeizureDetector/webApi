import { Theme } from "@mui/material";
import { createStyles, makeStyles } from '@mui/styles';

export const primary = "#6BBCF9";
export const secondary = "#30307D";
export const accent = "#0000BB";

export const useStyles = makeStyles((theme: Theme) => 
    createStyles({
        container: {
            display: 'flex',
            flexWrap: 'wrap',
            flexDirection: 'column',
            alignItems: 'center'
        },
        loginBtn: {
            marginTop: 16,
            flexGrow: 1,
        },
        header: {
            textAlign: 'center',
            background: secondary,
            color: '#fff'
        },
        card: {
            marginTop: '5%',
            maxWidth: '90%'
        },
        actions: {
            padding: '8px 16px!important'
        },
        row: {
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center'
        },
        minimiseWidth: {
            width: 'max-content'
        }
    })
);