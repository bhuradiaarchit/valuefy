import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PromptResponse {
  id: string;
  prompt: string;
  response: string;
  timestamp: number;
}

interface PromptState {
  responses: PromptResponse[];
  isLoading: boolean;
  error: string | null;
}

const initialState: PromptState = {
  responses: [],
  isLoading: false,
  error: null
};

const promptSlice = createSlice({
  name: 'prompt',
  initialState,
  reducers: {
    addResponse: (state, action: PayloadAction<PromptResponse>) => {
      state.responses.push(action.payload);
    },
    setPromptLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setPromptError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearResponses: (state) => {
      state.responses = [];
    },
    logoutPrompt: (state) => {
      state.responses = [];
      state.error = null;
      state.isLoading = false;
    }
  }
});

export const { addResponse, setPromptLoading, setPromptError, clearResponses ,logoutPrompt} = promptSlice.actions;
export default promptSlice.reducer;