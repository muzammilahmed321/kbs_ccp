import { Mail, Github, Linkedin } from "lucide-react";
import { siteConfig } from "../config/siteConfig.js";

export default function Contact() {
  const { email, github, linkedin } = siteConfig.contact;
  const items = [
    { icon: Mail, label: "Email", value: email, href: `mailto:${email}` },
    { icon: Github, label: "GitHub", value: "View the source code", href: github },
    { icon: Linkedin, label: "LinkedIn", value: "Connect with us", href: linkedin },
  ];
  return (
    <section id="contact" className="section">
      <div className="container">
        <p className="eyebrow">Contact</p>
        <h2>Get in Touch</h2>
        <div className="contact-grid">
          {items.map(({ icon: Icon, label, value, href }) => (
            <a className="contact-card card" key={label} href={href} target="_blank" rel="noreferrer">
              <span className="icon-badge">
                <Icon size={24} />
              </span>
              <div>
                <h3>{label}</h3>
                <p>{value}</p>
              </div>
            </a>
          ))}
        </div>
        <p className="course-note">
          {siteConfig.course} · {siteConfig.department}
        </p>
      </div>
    </section>
  );
}
