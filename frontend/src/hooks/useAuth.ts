import { useContext } from 'react';
import { AuthStateContext } from '../context/AuthStateContext';

export const useAuth = () => useContext(AuthStateContext);
