import { createContext, useState } from 'react';

export const AuthStateContext = createContext<AuthState>({
    isLoggedIn: false,
});

export const AuthStateProvider = (props: AuthStateProviderProps) => {
    const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

    const login = (token: string) => {
        localStorage.setItem('token', token);
        setToken(token);
        console.log(token);
    };

    const logout = () => {
        localStorage.clear();
        setToken(null);
    };

    const contextValue = {
        token,
        isLoggedIn: token !== null,
        login,
        logout,
    };

    return (
        <AuthStateContext.Provider value={contextValue}>{props.children}</AuthStateContext.Provider>
    );
};

interface AuthStateProviderProps {
    children: React.ReactNode;
}

interface AuthState {
    token?: string | null;
    isLoggedIn: boolean;
    login?: (token: string) => void;
    logout?: () => void;
}