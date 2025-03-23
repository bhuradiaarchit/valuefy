import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { BarChart3, MessageCircle, TrendingUp } from "lucide-react";
import { fetchGainersLosers, fetchHighVolumers } from "../services/api";
import "../styles/dashboard.css";
import { Skeleton } from "@mui/material";
import { useNavigate } from "react-router-dom";

function formatNumber(num) {
  if (num >= 1e9) return (num / 1e9).toFixed(2) + "B";
  if (num >= 1e6) return (num / 1e6).toFixed(2) + "M";
  if (num >= 1e3) return (num / 1e3).toFixed(2) + "K";
  return num.toString();
}

export default function Dashboard() {
  const [highVolumers, setHighVolumers] = useState([]);
  const [gainers, setGainers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadData() {
      try {
        const [volumeData, gainersData] = await Promise.all([
          fetchHighVolumers(),
          fetchGainersLosers(),
        ]);

        const highVolumersArray = Object.keys(volumeData.data.symbol).map((key) => ({
          symbol: volumeData.data.symbol[key],
          volume: volumeData.data.total_volume[key],
        }));
        
        setHighVolumers(highVolumersArray);
        setGainers(gainersData.data);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 space-y-6 mb-20">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="bg-blue-500 shadow-md rounded-lg p-4 mb-6 flex items-center gap-3">
          <BarChart3 className="text-white" size={24} />
          <h3 className="text-lg font-semibold text-slate-100">Dashboard</h3>
        </div>
      </motion.div>

       {/* Market Insights */}
       <div className="insights-card px-4 py-2 bg-slate-100 text-gray-700 shadow rounded-lg  flex items-center justify-between">
        <div>
          <h4 className="text-lg font-semibold">Latest Stock Market Data</h4>
          <p className="text-sm opacity-80">Get the latest trends and insights from our chatbot.</p>
        </div>
        <button onClick={()=>navigate("/chat-bot")} className="flex items-center gap-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 font-semibold px-5 py-2.5 rounded-lg shadow-md hover:opacity-80 transition">
  <MessageCircle size={20} className="text-blue-500" /> Chat with AI
</button>


      </div>

      <div className="grid">
        {/* High Volumers */}
        <div className="card">
          <div className="card-header">
            <BarChart3 className="text-blue-600" size={20} />
            <span className="card-title">Highest Activity of Institutions</span>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th className="volume-value">Volume</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  Array.from({ length: 5 }).map((_, index) => (
                    <tr key={index}>
                      <td><Skeleton variant="text" width={80} /></td>
                      <td className="text-right"><Skeleton variant="text" width={50} /></td>
                    </tr>
                  ))
                ) : (
                  highVolumers.map(({ symbol, volume }, index) => (
                    <tr key={index}>
                      <td>{symbol}</td>
                      <td className="volume-value">{formatNumber(volume)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Max Gainers */}
        <div className="card">
          <div className="card-header">
            <TrendingUp className="text-green-600" size={20} />
            <span className="card-title">Max Gainers by Hedge Funds</span>
          </div>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th className="change-value">Change</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  Array.from({ length: 5 }).map((_, index) => (
                    <tr key={index}>
                      <td><Skeleton variant="text" width={80} /></td>
                      <td className="text-right"><Skeleton variant="text" width={50} /></td>
                    </tr>
                  ))
                ) : (
                  gainers.map(([symbol, change], index) => (
                    <tr key={index}>
                      <td>{symbol}</td>
                      <td className={`change-value ${change >= 0 ? "positive" : "negative"}`}>
                        {change >= 0 ? "+" : ""}{change.toFixed(2)}%
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}