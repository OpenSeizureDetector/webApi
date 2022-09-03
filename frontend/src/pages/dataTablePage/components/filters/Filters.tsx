import { useDevice } from '../../../../hooks/useDevice';
import { Device } from '../../../../types/Device';
import { DesktopFilters } from './DesktopFilters';
import { MobileFilters } from './MobileFilters';

export const Filters = () => {
    const device = useDevice();

    return device === Device.DESKTOP ? <DesktopFilters /> : <MobileFilters />;
};
