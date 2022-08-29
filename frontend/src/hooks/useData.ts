import { useContext } from 'react';
import { EventDataContext } from '../context/EventDataContext';

export const useData = () => useContext(EventDataContext);
