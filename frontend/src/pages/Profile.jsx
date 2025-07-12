import React, { useEffect, useState } from "react";

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetch("https://cognivault.fly.dev/profile")
      .then((res) => res.json())
      .then((data) => setProfile(data))
      .catch((err) => console.error("❌ Profile fetch error:", err));
  }, []);

  return (
    <div>
      <h2>👤 Profile</h2>
      {profile ? (
        <pre style={{ background: "#222", padding: "20px", borderRadius: "6px" }}>
          {JSON.stringify(profile, null, 2)}
        </pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Profile;
