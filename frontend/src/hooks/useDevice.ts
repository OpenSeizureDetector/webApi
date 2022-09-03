import { useEffect, useState } from 'react';
import { getDevice } from '../types/Device';

export const useDevice = () => {
    const [width, setWidth] = useState(window.innerWidth);

    const handleWindowResize = () => setWidth(window.innerWidth);

    useEffect(() => {
        window.addEventListener('resize', handleWindowResize);

        return () => window.removeEventListener('resize', handleWindowResize);
    }, []);

    return getDevice(width);
};
