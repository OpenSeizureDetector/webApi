import { DriveFileRenameOutlineSharp } from '@mui/icons-material';
import { createContext, useContext, useEffect, useState } from 'react';
import { EventRepository } from '../data/eventRepository';
import { Event } from '../types/Event';
import { Filters } from '../types/Filters';
import { AuthStateContext } from './AuthStateContext';

const defaultFilters = {
    alarmState: [],
    eventType: [],
};

export const EventDataContext = createContext<EventDataState>({
    isLoading: true,
    filteredData: [],
    filters: defaultFilters,
    setFilters: () => {
        return;
    },
    clearFilters: () => {
        return;
    },
    eventTypes: {},
    data: [],
    setData: () => {
        return;
    },
});

export const EventDataProvider = (props: EventDataProviderProps) => {
    const [isLoading, setLoading] = useState(true);
    const [data, setData] = useState<Event[]>([]);
    const [filters, setFilters] = useState<Filters>({
        alarmState: [],
        eventType: [],
    });
    const [filteredData, setFilteredData] = useState<Event[]>([]);
    const [eventTypes, setEventTypes] = useState({});

    const { token } = useContext(AuthStateContext);

    const clearFilters = () => setFilters(defaultFilters);

    const contextValue = {
        isLoading,
        filters,
        filteredData,
        setFilters,
        clearFilters,
        eventTypes,
        data,
        setData,
    };

    useEffect(() => {
        setLoading(true);
        new EventRepository(token ?? '').getEventTypes().then(setEventTypes);
        new EventRepository(token ?? '').getAllEvents().then((response) => {
            setData(response);
            setLoading(false);
        });
    }, [token]);

    useEffect(() => {
        setFilteredData(
            data
                .filter((dataPoint: Event) =>
                    filters.alarmState.length === 0
                        ? true
                        : filters.alarmState.includes(dataPoint.alarmState)
                )
                .filter((dataPoint: Event) =>
                    filters.eventType.length === 0
                        ? true
                        : filters.eventType.includes(dataPoint.type)
                )
                .filter((dataPoint: Event) =>
                    filters.startDate ? filters.startDate <= dataPoint.date : true
                )
                .filter((dataPoint: Event) =>
                    filters.endDate ? filters.endDate >= dataPoint.date : true
                )
                .filter((dataPoint: Event) =>
                    filters.userId ? filters.userId === dataPoint.userId : true
                )
        );
    }, [data, filters]);

    return (
        <EventDataContext.Provider value={contextValue}>{props.children}</EventDataContext.Provider>
    );
};

interface EventDataProviderProps {
    children: React.ReactNode;
}

interface EventDataState {
    isLoading: boolean;
    filteredData: Event[];
    filters: Filters;
    setFilters: (value: Filters) => void;
    clearFilters: () => void;
    eventTypes: Record<string, string[]>;
    data: Event[];
    setData: (value: Event[]) => void;
}
