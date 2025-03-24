import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface User {
  username: string;
}

interface AuthState {
  currentUser: User | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  currentUser: null,
  isLoading: false,
  error: null
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User | null>) => {
      state.currentUser = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    logoutAuth: (state) => {
      state.currentUser = null;
      state.error = null;
      state.isLoading = false;
    }
  }
});

export const { setUser, setLoading, setError, logoutAuth } = authSlice.actions;
export default authSlice.reducer;