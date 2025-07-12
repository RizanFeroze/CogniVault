import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Goals = () => {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/goals`)
      .then((res) => {
        if (!res.ok) throw new Error("Server error");
        return res.json();
      })
      .then((data) => {
        console.log("✅ Goals loaded:", data);
        setGoals(data);
      })
      .catch((err) => {
        console.error("❌ Goals fetch error:", err);
        alert("Failed to load goals from server.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>🎯 Goals</h2>

      {loading ? (
        <p>Loading goals...</p>
      ) : goals.length > 0 ? (
        goals.map((g, i) => (
          <div
            key={i}
            style={{
              background: "#222",
              padding: "12px",
              marginBottom: "10px",
              borderRadius: "6px",
            }}
          >
            <p><strong>{g.goal}</strong></p>
            <p>Status: {g.status}</p>
            <small>{new Date(g.created_at).toLocaleString()}</small>
          </div>
        ))
      ) : (
        <p>No goals yet.</p>
      )}
    </div>
  );
};

export default Goals;
