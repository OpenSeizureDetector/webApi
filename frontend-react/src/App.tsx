import { Routing } from './router/router';
import { RecoilRoot } from 'recoil';
import { createTheme, ThemeProvider } from '@mui/material';
import { accent, primary, secondary } from './pages/styles';

function App() {

  let theme = createTheme({
    palette: {
      primary: {
        main: primary
      },
      secondary: {
        main: secondary
      },
      info: {
        main: accent
      }
    }
  });

  return (
    <RecoilRoot>
      <ThemeProvider theme={theme}>
        <Routing />
      </ThemeProvider>
    </RecoilRoot>
  );
}

export default App;
