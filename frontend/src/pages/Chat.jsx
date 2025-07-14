import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Chat = () => {
  const [memories, setMemories] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Load memory history on mount
  useEffect(() => {
    fetch(`${API_BASE}/chat`)
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Loaded chat history:", data);
        setMemories(data);
      })
      .catch((err) => console.error("❌ Fetch error (GET /chat):", err));
  }, []);

  const handleSubmit = async () => {
    if (!newMessage.trim()) return;

    const userText = newMessage;
    const timestamp = new Date().toISOString();

    const userBubble = {
      role: "user",
      text: userText,
      timestamp,
    };

    setMemories((prev) => [...prev, userBubble]);
    setNewMessage("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "devuser", text: userText }),
      });

      const data = await res.json();

      const aiBubble = {
        role: "assistant",
        text: data.reply || "⚠️ No response from AI.",
        timestamp: new Date().toISOString(),
      };

      setMemories((prev) => [...prev, aiBubble]);

      // Optional: save to /memories
      const memoryPayload = {
        username: "devuser",
        text: userText,
        emotion: "Reflective",
        cognition: "Memory",
        label: "Chat",
        theme: "Simulation",
        timestamp,
        linked_goals: [],
      };
      await fetch(`${API_BASE}/memories`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(memoryPayload),
      });

    } catch (err) {
      console.error("❌ POST /chat error:", err);
      setMemories((prev) => [
        ...prev,
        { role: "assistant", text: "⚠️ AI failed to respond.", timestamp: new Date().toISOString() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>💬 Chat with AI</h2>
      <div style={{ marginBottom: "20px" }}>
        {memories.map((m, i) => (
          <div
            key={i}
            style={{
              background: m.role === "assistant" ? "#333" : "#1e88e5",
              color: "#fff",
              padding: "10px",
              borderRadius: "6px",
              margin: "6px 0",
              textAlign: m.role === "assistant" ? "left" : "right",
            }}
          >
            {m.text}
            <div style={{ fontSize: "0.8em", marginTop: "4px", opacity: 0.6 }}>
              {new Date(m.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        {loading && <div>🤖 Thinking...</div>}
      </div>

      <div>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Ask the AI something..."
          style={{ width: "70%", padding: "8px" }}
        />
        <button onClick={handleSubmit} style={{ padding: "8px 16px", marginLeft: "10px" }}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
