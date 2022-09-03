export enum Device {
    MOBILE = 'Mobile',
    TABLET = 'Tablet',
    DESKTOP = 'Desktop',
}

export const getDevice = (width: number) => {
    if (width <= 480) return Device.MOBILE;
    if (width <= 1024) return Device.TABLET;
    return Device.DESKTOP;
};
