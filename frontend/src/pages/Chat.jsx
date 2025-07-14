import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Chat = () => {
  const [memories, setMemories] = useState([]);
  const [newMemory, setNewMemory] = useState("");
  const [aiReply, setAiReply] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/chat`)
      .then((res) => res.json())
      .then((data) => setMemories(data))
      .catch((err) => console.error("❌ Fetch error (GET /chat):", err));
  }, []);

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

    // Save memory
    fetch(`${API_BASE}/memories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(memoryData),
    })
      .then((res) => res.json())
      .then(() => {
        setMemories((prev) => [...prev, memoryData]);
        setNewMemory("");

        // Call AI
        fetch(`${API_BASE}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: "devuser", text: memoryData.text }),
        })
          .then((res) => res.json())
          .then((data) => {
            const aiMessage = {
              username: "ai",
              text: data.reply,
              timestamp: new Date().toISOString(),
            };
            setMemories((prev) => [...prev, aiMessage]);
            setAiReply(data.reply);
          })
          .catch((err) => console.error("❌ GPT request failed:", err));
      });
  };

  return (
    <div>
      <h2>🧠 Chat with AI</h2>
      <input
        type="text"
        value={newMemory}
        onChange={(e) => setNewMemory(e.target.value)}
        placeholder="Ask something..."
        style={{ padding: "10px", width: "60%" }}
      />
      <button onClick={handleSubmit} style={{ padding: "10px 20px", marginLeft: "10px" }}>
        Send
      </button>

      <div style={{ marginTop: "20px" }}>
        {memories.map((m, i) => (
          <div
            key={i}
            style={{
              background: m.username === "ai" ? "#444" : "#222",
              color: "white",
              marginBottom: "12px",
              padding: "10px",
              borderRadius: "6px",
            }}
          >
            <strong>{m.username === "ai" ? "🤖 AI" : "🧍 You"}:</strong> {m.text}
            <div style={{ fontSize: "12px", opacity: 0.6 }}>{new Date(m.timestamp).toLocaleString()}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chat;
