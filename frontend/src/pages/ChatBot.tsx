import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import { CircularProgress, TextField, Button } from "@mui/material";
import { Send } from "lucide-react";
import { toast } from "react-hot-toast";
import { addResponse, setPromptLoading, setPromptError } from "../store/slices/promptSlice";
import { RootState } from "../store/store";
import Plot from "react-plotlyjs";
import { getChatResponse } from "../services/api";

const ChatBot = () => {
  const [prompt, setPrompt] = useState("");
  const dispatch = useDispatch();
  const { responses, isLoading } = useSelector((state: RootState) => state.prompt);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) {
      toast.error("Please enter a prompt");
      return;
    }

    dispatch(setPromptLoading(true));
    try {
      const response = await getChatResponse(prompt);
      console.log(response);
      
      dispatch(addResponse(response));
      setPrompt("");
      toast.success("Analysis received!");
    } catch (error) {
      dispatch(setPromptError((error as Error).message));
      toast.error("Failed to get insights");
    } finally {
      dispatch(setPromptLoading(false));
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Data Chatbot</h1>
        <p className="text-lg text-gray-600">Ask anything about data insights and analysis.</p>
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
            className="bg-white rounded-lg"
          />
          <Button type="submit" variant="contained" disabled={isLoading} className="px-6">
            {isLoading ? <CircularProgress size={24} /> : <Send size={20} />}
          </Button>
        </div>
      </form>

      <div className="space-y-6">
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
            <h3 className="text-lg font-semibold">SQL Query:</h3>
            <pre className="bg-gray-100 p-2 rounded-md overflow-x-auto">{response.query}</pre>

            {response.data && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold">Data Table:</h3>
                <div className="overflow-auto">
                  <table className="w-full border-collapse border border-gray-300">
                    <thead>
                      <tr className="bg-gray-200">
                        {Object.keys(response.data).map((key) => (
                          <th key={key} className="border p-2">{key}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {response.data[Object.keys(response.data)[0]].map((_, rowIndex) => (
                        <tr key={rowIndex} className="border">
                          {Object.keys(response.data).map((key) => (
                            <td key={key} className="border p-2">
                              {response.data[key][rowIndex]}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {response.figure && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold">Plot:</h3>
                <Plot data={response.figure.data} layout={response.figure.layout} />
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ChatBot;
