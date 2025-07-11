import React, { useEffect, useState } from "react";

const Insights = () => {
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/insights")
      .then((res) => res.json())
      .then((data) => setInsights(data))
      .catch((err) => console.error("❌ Insights fetch error:", err));
  }, []);

  return (
    <div>
      <h2>📊 Insights</h2>
      {insights.length > 0 ? (
        <ul>
          {insights.map((item, i) => (
            <li key={i} style={{ marginBottom: "10px" }}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>No insights available.</p>
      )}
    </div>
  );
};

export default Insights;
