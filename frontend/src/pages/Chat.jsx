import React, { useEffect, useState } from "react";

const Chat = () => {
  const [memories, setMemories] = useState([]);
  const [newMemory, setNewMemory] = useState("");

  // Load memory history on mount
  useEffect(() => {
    fetch("https://cognivault.fly.dev/chat")
      .then((res) => res.json())
      .then((data) => setMemories(data))
      .catch((err) => console.error("❌ Fetch error:", err));
  }, []);

  // Submit new memory
  const handleSubmit = () => {
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

    fetch(fetch("https://cognivault.fly.dev/memories")
    , {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(memoryData),
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.status === "success") {
          setMemories([...memories, memoryData]);
          setNewMemory("");
        }
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
