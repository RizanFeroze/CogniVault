import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Chat from "./pages/Chat";
import Goals from "./pages/Goals";
import Profile from "./pages/Profile";
import Insights from "./pages/Insights";

const App = () => {
  return (
    <Router>
      <nav style={{ padding: "12px", background: "#121212", color: "#fff", display: "flex", gap: "16px" }}>
        <Link to="/" style={{ marginRight: "10px" }}>Chat</Link>
        <Link to="/goals" style={{ marginRight: "10px" }}>Goals</Link>
        <Link to="/insights" style={{ marginRight: "10px" }}>Insights</Link>
        <Link to="/profile">Profile</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/goals" element={<Goals />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  );
};

export default App;
