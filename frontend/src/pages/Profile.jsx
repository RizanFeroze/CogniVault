import React, { useEffect, useState } from "react";
import API_BASE from "../config";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/profile`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch profile");
        return res.json();
      })
      .then((data) => {
        console.log("✅ Profile fetched:", data);
        setProfile(data);
      })
      .catch((err) => {
        console.error("❌ Profile fetch error:", err);
        setError("Unable to load profile. Please try again later.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>👤 Profile</h2>

      {loading && <p>Loading profile...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {profile && (
        <pre
          style={{
            background: "#222",
            padding: "20px",
            borderRadius: "6px",
            whiteSpace: "pre-wrap",
            wordWrap: "break-word",
            overflowX: "auto",
          }}
        >
          {JSON.stringify(profile, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default Profile;
