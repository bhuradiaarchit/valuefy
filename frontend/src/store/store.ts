import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import authReducer from './slices/authSlice';
import promptReducer from './slices/promptSlice';

const authPersistConfig = {
  key: 'auth',
  storage,
  whitelist: ['currentUser']
};

const promptPersistConfig = {
  key: 'prompt',
  storage,
  whitelist: ['responses'] // Persisting only responses
};

export const store = configureStore({
  reducer: {
    auth: persistReducer(authPersistConfig, authReducer),
    prompt: persistReducer(promptPersistConfig, promptReducer)
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false
    })
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
