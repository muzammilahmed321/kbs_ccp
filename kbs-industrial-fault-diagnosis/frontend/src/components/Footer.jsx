import { Mail, Github, Linkedin } from "lucide-react";
import Logo from "./Logo.jsx";
import { siteConfig } from "../config/siteConfig.js";

export default function Footer() {
  const { email, github, linkedin } = siteConfig.contact;
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <div>
          <Logo />
          <p className="footer-tag">{siteConfig.tagline}</p>
        </div>
        <div className="footer-links">
          <a href="#contact">Contact Us</a>
          <a className="social" href={github} target="_blank" rel="noreferrer" aria-label="GitHub">
            <Github size={22} />
          </a>
          <a className="social" href={linkedin} target="_blank" rel="noreferrer" aria-label="LinkedIn">
            <Linkedin size={22} />
          </a>
          <a className="social" href={`mailto:${email}`} aria-label="Email">
            <Mail size={22} />
          </a>
        </div>
      </div>
      <p className="copyright">© {new Date().getFullYear()} {siteConfig.brand}. {siteConfig.course}.</p>
    </footer>
  );
}
