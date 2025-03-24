import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import { CircularProgress, TextField, Button } from "@mui/material";
import { Send } from "lucide-react";
import { toast } from "react-hot-toast";
import { addResponse, setPromptLoading, setPromptError } from "../store/slices/promptSlice";
import { RootState } from "../store/store";
import Plot from "react-plotly.js";
import { getChatResponse } from "../services/api";
import "../styles/chatbot.css";

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
      toast.success("Analysis received!");
    } catch (error) {
      dispatch(setPromptError((error as Error).message));
      toast.error("Failed to get insights");
    } finally {
      dispatch(setPromptLoading(false));
    }
  };

  const downloadCSV = (data: any) => {
    const headers = "Symbol,Total Volume\n";
    const rows = Object.keys(data.symbol)
      .map((index) => `${data.symbol[index]},${data.total_volume[index]}`)
      .join("\n");
    
    const csvContent = "data:text/csv;charset=utf-8," + headers + rows;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "data_table.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
            <p className="text-gray-700 font-medium mb-4">{response.prompt}</p>
            <h3 className="text-lg font-semibold">SQL Query:</h3>
            <pre className="bg-gray-100 p-2 rounded-md overflow-x-auto">{response.query}</pre>

            {response.data && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold">Data Table:</h3>
                <button
                  className="bg-blue-500 text-white px-4 py-2 rounded-md mb-2"
                  onClick={() => downloadCSV(response.data)}
                >
                  Download CSV
                </button>
                <div className="overflow-auto">
                  <table className="w-full border-collapse border border-gray-300">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="border p-2">Symbol</th>
                        <th className="border p-2">Total Volume</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.keys(response.data.symbol).slice(0, 10).map((index) => (
                        <tr key={index} className="border">
                          <td className="border p-2">{response.data.symbol[index]}</td>
                          <td className="border p-2">{response.data.total_volume[index]}</td>
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
                <Plot
                  data={response.figure.data}
                  layout={response.figure.layout}
                  style={{ width: "100%", height: "400px" }}
                  config={{ responsive: true }}
                />
              </div>
            )}

          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ChatBot;
