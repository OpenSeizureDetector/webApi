import { useContext, useEffect, useState } from 'react';
import { AuthStateContext } from '../context/AuthStateContext';
import { EventRepository } from '../data/auth/eventRepository';

export const useData = () => {
    const [isLoading, setLoading] = useState(true);
    const [data, setData] = useState<Event[]>([]);

    const { token } = useContext(AuthStateContext);

    useEffect(() => {
        new EventRepository(token ?? '').getAllEvents().then((response) => {
            setData(response);
            setLoading(false);
        });
    }, []);

    return { isLoading, data };
};
