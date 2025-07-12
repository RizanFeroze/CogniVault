import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Chat = () => {
  const [memories, setMemories] = useState([]);
  const [newMemory, setNewMemory] = useState("");

  // Load memory history on mount
  useEffect(() => {
    fetch(`${API_BASE}/chat`)
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Loaded chat memories:", data);
        setMemories(data);
      })
      .catch((err) => console.error("❌ Fetch error (GET /chat):", err));
  }, []);

  // Handle memory submit
  const handleSubmit = () => {
    if (!newMemory.trim()) return;

    const memoryData = {
      username: "devuser",
      text: newMemory,
      emotion: "Reflective",
      cognition: "Memory",
      label: "Chat",
      theme: "Simulation",
      timestamp: new Date().toISOString(),
      linked_goals: [],
    };

    fetch(`${API_BASE}/memories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(memoryData),
    })
      .then((res) => res.json())
      .then((response) => {
        console.log("✅ Response from POST /memories:", response);

        // Accept both strict and fallback success conditions
        if (response.status === "success" || response.ok || response.detail === "Memory added") {
          setMemories((prev) => [...prev, memoryData]);
          setNewMemory("");
        } else {
          console.error("⚠️ Unexpected POST response:", response);
          alert("Something went wrong saving your memory.");
        }
      })
      .catch((err) => {
        console.error("❌ POST /memories failed:", err);
        alert("Error submitting memory. Try again.");
      });
  };

  return (
    <div>
      <h2>🧠 Chat Page</h2>
      <div style={{ margin: "20px 0" }}>
        <input
          type="text"
          value={newMemory}
          onChange={(e) => setNewMemory(e.target.value)}
          placeholder="Write a thought..."
          style={{
            padding: "10px",
            width: "60%",
            marginRight: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
        <button onClick={handleSubmit} style={{ padding: "10px 20px" }}>
          Send
        </button>
      </div>

      <div>
        {memories.map((mem, index) => (
          <div
            key={index}
            style={{
              background: "#222",
              marginBottom: "10px",
              padding: "12px",
              borderRadius: "6px",
            }}
          >
            <p>{mem.text}</p>
            <small>{new Date(mem.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chat;
