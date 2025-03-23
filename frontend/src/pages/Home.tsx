import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { CircularProgress, TextField, Button } from '@mui/material';
import { Send } from 'lucide-react';
import { toast } from 'react-hot-toast';
import { addResponse, setPromptLoading, setPromptError } from '../store/slices/promptSlice';
import { getStockInsights } from '../services/api';
import { RootState } from '../store/store';

const Home = () => {
  const [prompt, setPrompt] = useState('');
  const dispatch = useDispatch();
  const { responses, isLoading } = useSelector((state: RootState) => state.prompt);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) {
      toast.error('Please enter a prompt');
      return;
    }

    dispatch(setPromptLoading(true));
    try {
      const response = await getStockInsights(prompt);
      dispatch(addResponse(response));
      setPrompt('');
      toast.success('Analysis received!');
    } catch (error) {
      dispatch(setPromptError((error as Error).message));
      toast.error('Failed to get insights');
    } finally {
      dispatch(setPromptLoading(false));
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Stock Market AI Assistant</h1>
        <p className="text-lg text-gray-600">
          Ask me anything about stocks, market trends, or investment strategies.
        </p>
      </motion.div>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-2">
          <TextField
            fullWidth
            variant="outlined"
            placeholder="e.g., Analyze the current tech sector trends..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isLoading}
            className="bg-white"
          />
          <Button
            type="submit"
            variant="contained"
            disabled={isLoading}
            className="px-6"
          >
            {isLoading ? <CircularProgress size={24} /> : <Send size={20} />}
          </Button>
        </div>
      </form>

      <div className="space-y-4">
        {responses.map((response) => (
          <motion.div
            key={response.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <p className="text-sm text-gray-500 mb-2">
              {new Date(response.timestamp).toLocaleString()}
            </p>
            <p className="text-gray-700 font-medium mb-4">{response.prompt}</p>
            <p className="text-gray-900">{response.response}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Home;