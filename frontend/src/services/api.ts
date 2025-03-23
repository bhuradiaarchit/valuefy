import { toast } from 'react-hot-toast';
import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

const API_DELAY = 1000; // Simulated API delay

export const loginUser = async (username: string, password: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, {
      username,
      password,
    });
c
    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    const errorMessage = error?.response?.data?.error || "Login failed";
    console.log(errorMessage);
    
    throw new Error(errorMessage);
  }
};

export const registerUser = async (username: string, password: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/signup`, {
      username,
      password,
    });

    return response.data;
  } catch (error) {
    console.error("Registration failed:", error);
    throw new Error("Registration failed");
  }
};

export const getStockInsights = async (prompt: string) => {
  await new Promise(resolve => setTimeout(resolve, API_DELAY));
  
  // Simulate API response
  return {
    id: Date.now().toString(),
    prompt,
    response: `Analysis for "${prompt}": Market trends indicate positive momentum in tech sector. Consider diversifying portfolio with focus on AI and renewable energy stocks.`,
    timestamp: Date.now()
  };
};


export const getChatResponse = async (message: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { message });

    return response.data; // Expected to contain SQL query, table data, and plot JSON
  } catch (error) {
    console.error("Error fetching chat response:", error);
    throw new Error("Failed to fetch response from the server");
  }
};

export const fetchMarketNews = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/analyze-news`);
    return response.data;
  } catch (error) {
    console.error("Error fetching market news:", error);
    throw new Error("Failed to fetch market news");
  }
};

export const fetchHighVolumers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/high-volumers`);
    return response.data;
  } catch (error) {
    console.error("Error fetching high volumers:", error);
    throw new Error("Failed to fetch high volumers");
  }
};

export const fetchGainersLosers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/gainers-losers`);
    return response.data;
  } catch (error) {
    console.error("Error fetching gainers/losers:", error);
    throw new Error("Failed to fetch gainers/losers");
  }
};