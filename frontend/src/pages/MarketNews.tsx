import React, { useEffect, useState } from "react";
import { Newspaper } from "lucide-react";
import { fetchMarketNews } from "../services/api";
import { motion } from "framer-motion";
import { Skeleton } from "@mui/material";

export default function MarketNews() {
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNews() {
      try {
        const response = await fetchMarketNews();
        setNews(response.data);
      } catch (error) {
        console.error("Error fetching market news:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="bg-blue-500 shadow-md rounded-lg p-4 mb-6">
          <div className="flex items-center gap-3">
            <Newspaper className="text-white" size={24} />
            <h3 className="text-lg font-semibold text-slate-100">Market News</h3>
            <span className="ml-auto bg-blue-100/70 backdrop-blur-md text-blue-800 px-3 py-1 rounded-full text-xs font-medium border border-white/50">
              {news.length} updates
            </span>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
           Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="bg-white shadow-md p-4 rounded-lg">
              <Skeleton variant="text" width="80%" height={20} />
              <Skeleton variant="rectangular" height={60} className="mt-2" />
            </div>
          ))
        ) : (
          news.map((item, index) => {
            const type = item.recommendation.includes("BUY")
              ? "buy"
              : item.recommendation.includes("SELL")
              ? "sell"
              : "hold";

            return (
              <div
                key={index}
                className={`news-card ${type} bg-white p-4 rounded-lg shadow-md border-l-4 transition-transform transform hover:-translate-y-1 hover:shadow-lg`}
              >
                <h4 className="news-title text-lg font-semibold mb-2 line-clamp-2">
                  {item.title}
                </h4>
                <p className="news-content text-gray-600 text-sm mb-3 line-clamp-3">
                  {item.content}
                </p>
                <span className={`news-badge ${type} px-3 py-1 rounded-full text-xs font-medium`}>{item.recommendation}</span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
