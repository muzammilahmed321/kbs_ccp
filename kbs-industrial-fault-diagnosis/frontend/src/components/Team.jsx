import { useState } from "react";
import { siteConfig } from "../config/siteConfig.js";

function initials(name) {
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

function Member({ name, role, photo }) {
  const [failed, setFailed] = useState(!photo);
  return (
    <div className="member">
      <div className="avatar">
        {failed ? (
          <span>{initials(name)}</span>
        ) : (
          <img src={photo} alt={name} onError={() => setFailed(true)} />
        )}
      </div>
      <h3>{name}</h3>
      <p>{role}</p>
    </div>
  );
}

export default function Team() {
  return (
    <section id="team" className="section">
      <div className="container">
        <p className="eyebrow">Our Team</p>
        <h2>Meet the Team</h2>
        <div className="team-grid">
          {siteConfig.team.map((m) => (
            <Member key={m.name} {...m} />
          ))}
        </div>
      </div>
    </section>
  );
}
