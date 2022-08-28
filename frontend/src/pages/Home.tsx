import { Button } from '@mui/material';
import { useContext, useEffect, useState } from 'react';
import { AuthStateContext } from '../context/AuthStateContext';
import { EventRepository } from '../data/auth/eventRepository';

export const Home = () => {
    const { token, logout } = useContext(AuthStateContext);

    const [data, setData] = useState([]);

    useEffect(() => {
        new EventRepository(token ?? '').getAllEvents().then(setData);
    }, []);

    console.log(data);

    return (
        <div>
            <Button onClick={logout}>Logout</Button>
        </div>
    );
};
