import { ArrowRight, Play, Thermometer, Gauge, Activity, Clock3 } from "lucide-react";
import { siteConfig } from "../config/siteConfig.js";

const sensorInputs = [
  { name: "Air Temperature", icon: Thermometer },
  { name: "Process Temperature", icon: Thermometer },
  { name: "Rotational Speed", icon: Gauge },
  { name: "Torque", icon: Activity },
  { name: "Tool Wear", icon: Clock3 },
];

export default function Hero() {
  const { tagline, heroImage, liveDemoUrl } = siteConfig;
  return (
    <section id="home" className="hero">
      <div className="hero-bg" style={{ backgroundImage: `url(${heroImage})` }} aria-hidden="true" />
      <div className="hero-shade" aria-hidden="true" />
      <div className="container hero-inner">
        <div className="hero-copy">
          <p className="hero-kicker"><span className="status-dot" /> INTELLIGENT INDUSTRIAL MONITORING</p>
          <h1>Industrial<br /><span className="accent">Fault</span> Detection</h1>
          <p className="hero-sub">{tagline}</p>
          <div className="hero-actions">
            <a className="btn btn-primary" href="/new-diagnosis">Try It Live <ArrowRight size={18} /></a>
            <a className="btn btn-outline" href="#demo"><Play size={17} /> Watch Demo</a>
          </div>
        </div>
        <div className="sensor-readings">
          <div className="sensor-readings-heading">
            <span className="sensor-heading-line" />
            <span> MACHINE SENSOR READINGS </span>
            <span className="sensor-heading-line" />
          </div>
          <div className="sensor-strip" aria-label="Five model input features">
          {sensorInputs.map(({ name, icon: Icon }, index) => (
            <div className="sensor-item" key={name}>
              <span className="sensor-index">0{index + 1}</span>
              <span className="sensor-glyph"><Icon size={25} strokeWidth={1.9} /></span>
              <span className="sensor-label">{name}</span>
            </div>
          ))}
          </div>
        </div>
      </div>
    </section>
  );
}
