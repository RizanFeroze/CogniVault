import React, { useEffect, useState } from "react";

const Goals = () => {
  const [goals, setGoals] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/goals")
      .then((res) => res.json())
      .then((data) => setGoals(data))
      .catch((err) => console.error("❌ Goals fetch error:", err));
  }, []);

  return (
    <div>
      <h2>🎯 Goals</h2>
      {goals.length > 0 ? (
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
            <small>{g.created_at}</small>
          </div>
        ))
      ) : (
        <p>No goals yet.</p>
      )}
    </div>
  );
};

export default Goals;
