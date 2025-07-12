import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Insights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/insights`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch insights");
        return res.json();
      })
      .then((data) => {
        console.log("✅ Insights fetched:", data);
        setInsights(data);
      })
      .catch((err) => {
        console.error("❌ Insights fetch error:", err);
        alert("Could not load insights. Please try again later.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>📊 Insights</h2>

      {loading ? (
        <p>Loading insights...</p>
      ) : insights.length > 0 ? (
        <ul style={{ paddingLeft: "20px" }}>
          {insights.map((item, i) => (
            <li
              key={i}
              style={{
                background: "#222",
                marginBottom: "10px",
                padding: "10px",
                borderRadius: "6px",
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p>No insights available.</p>
      )}
    </div>
  );
};

export default Insights;
