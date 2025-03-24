import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Button, CircularProgress, TextField } from "@mui/material";
import { Send } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { addResponse, setPromptLoading, setPromptError } from "../store/slices/promptSlice";
import { toast } from "react-hot-toast";
import PlotComponent from "../components/PlotComponent";
import { getChatResponse } from "../services/api";
import Loader from "../components/Loader";

const ChatBot = () => {
  const dispatch = useDispatch();
  const { responses, isLoading } = useSelector((state: RootState) => state.prompt);
  const [prompt, setPrompt] = useState("");
  const chatEndRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      toast.error("Please enter a prompt");
      return;
    }

    dispatch(setPromptLoading(true));

    // 1️⃣ Add user's message immediately
    const userMessage = { id: Date.now(), prompt, isUser: true };
    dispatch(addResponse(userMessage));

    // 2️⃣ Add a temporary "Thinking..." message (ID: -1)
    const thinkingMessage = { id: -1, prompt: "Thinking...", isUser: false };
    dispatch(addResponse(thinkingMessage));

    try {
      const response = await getChatResponse(prompt);

      // 3️⃣ Remove "Thinking..." by filtering it out
      dispatch(setPromptLoading(false));
      dispatch(addResponse({ ...response, id: Date.now(), prompt, isUser: false }));
    } catch (error) {
      dispatch(setPromptError(error.message));
      toast.error("Failed to get insights");
    } finally {
      dispatch(setPromptLoading(false));
    }

    setPrompt(""); // Clear input
  };


  // Scroll to the latest message when responses update
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [responses]);

  return (
    <div className="max-w-5xl mx-auto px-6">
      <div className="fixed top-0 bg-slate-50 z-10 text-center w-[80%]" >
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="my-4 text-center">
          <div className="text-5xl font-bold text-gray-900 mb-1 text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 hover:opacity-80 transition py-2">Chatbot by Valuefy</div>
          <p className="text-lg text-gray-600 font-mono">Ask anything about data insights and analysis.</p>
        </motion.div>

        {/* Input field */}
        <form onSubmit={handleSubmit} className="mb-4">
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
             <Send size={20} />
            </Button>
          </div>
        </form>
      </div>

      {/* Chat Messages */}
      <div className="space-y-4 overflow-y-auto p-4 bg-gray-100 rounded-lg mt-48">
        {Array.isArray(responses) && responses
          .filter((response, index, self) =>
            response.id !== -1 || self.findIndex((r) => r.id === -1) === index
          ) // Keep only one "Thinking..." message
          .map((response) => (
            <motion.div
              key={response.id}
              initial={{ opacity: 0, x: response.isUser ? 50 : -50 }}
              animate={{ opacity: 1, x: 0 }}
              className={`flex ${response.isUser ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`p-4 rounded-lg shadow-md max-w-[80%] ${response.isUser
                  ? "bg-blue-500 text-white self-end"
                  : "bg-white text-gray-700 self-start"
                  }`}
              >
                {
                  response.isUser && (
                    <p>{response.prompt}</p>
                  )
                }

                {!response.isUser && (
                  <>
                    <h3 className="text-lg font-semibold mt-2">Query:</h3>
                    <pre className="bg-gray-200 p-2 rounded-md overflow-x-auto">{response.query}</pre>

                    {response.data && response.data.symbol && response.data.total_volume && (
                      <div className="mt-2">
                        <h3 className="text-lg font-semibold">Data Table:</h3>
                        <div className="overflow-auto min-w-[300px] max-w-[600px]">
                          <table className="w-full border-collapse border border-gray-300">
                            <thead>
                              <tr className="bg-gray-200">
                                <th className="border p-2">Symbol</th>
                                <th className="border p-2">Total Volume</th>
                              </tr>
                            </thead>
                            <tbody>
                              {typeof response.data.symbol === "object" &&
                                typeof response.data.total_volume === "object" &&
                                Object.keys(response.data.symbol)
                                  .slice(0, 10)
                                  .map((key, index) => (
                                    <tr key={`data-row-${index}`} className="border">
                                      <td className="border p-2">{response.data.symbol[key]}</td>
                                      <td className="border p-2">{response.data.total_volume[key]}</td>
                                    </tr>
                                  ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}



                    {response.figure && (
                      <div className="mt-4 overflow-auto min-w-[500px] max-w-[600px]">
                        <h3 className="text-lg font-semibold">Plot:</h3>
                        <PlotComponent figure={response.figure} />
                      </div>
                    )}

                  </>
                )}
              </div>
            </motion.div>
          ))}
        {/* Loader message while fetching response */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="self-start bg-gray-200 text-gray-700 p-4 rounded-lg max-w-[80%] shadow-md flex items-center gap-2"
          >
            <div className="mr-4">Thinking...</div>
            <Loader />
          </motion.div>
        )}

        <div ref={chatEndRef} />
      </div>
    </div>
  );
};

export default ChatBot;
