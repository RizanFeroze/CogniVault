import React from "react";
import { Link, Outlet, useLocation } from "react-router-dom";
import "./Layout.css";

const Layout = () => {
  const location = useLocation();

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>🧠 CogniVault</h2>
        <nav>
          <Link to="/" className={location.pathname === "/" ? "active" : ""}>Chat</Link>
          <Link to="/profile" className={location.pathname === "/profile" ? "active" : ""}>Profile</Link>
          <Link to="/goals" className={location.pathname === "/goals" ? "active" : ""}>Goals</Link>
          <Link to="/insights" className={location.pathname === "/insights" ? "active" : ""}>Insights</Link>
        </nav>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
