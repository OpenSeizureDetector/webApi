import { createTheme } from '@mui/material';

const primary = '#30307D';
const secondary = '#6BBCF9';
const accent = '#0000BB';

export const theme = createTheme({
    palette: {
        primary: {
            main: primary,
        },
        secondary: {
            main: secondary,
        },
        info: {
            main: accent,
        },
    },
});
