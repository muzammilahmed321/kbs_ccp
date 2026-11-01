import { useState } from "react";
import {
  Activity, LayoutDashboard, PlusCircle, History, GitBranch,
  Settings, Bell, Search, ChevronDown, ArrowUpRight, Gauge,
  Thermometer, Zap, Wrench, Menu, X, CircleHelp
} from "lucide-react";
import Logo from "./Logo.jsx";
import { siteConfig } from "../config/siteConfig.js";

const NAV_ITEMS = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "New Diagnosis", icon: PlusCircle },
  { label: "History", icon: History },
  { label: "Rule System", icon: GitBranch },
  { label: "Settings", icon: Settings },
];

const INPUTS = [
  { label: "Air Temperature", field: "air_temperature", unit: "K", icon: Thermometer },
  { label: "Process Temperature", field: "process_temperature", unit: "K", icon: Thermometer },
  { label: "Rotational Speed", field: "rotational_speed", unit: "RPM", icon: Gauge },
  { label: "Torque", field: "torque", unit: "Nm", icon: Zap },
  { label: "Tool Wear", field: "tool_wear", unit: "min", icon: Wrench },
];

export default function Dashboard() {
  const [active, setActive] = useState("Overview");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="dashboard-page">
      <aside className={`dashboard-sidebar ${sidebarOpen ? "is-open" : ""}`}>
        <div className="dashboard-brand"><Logo /><button className="dashboard-close" onClick={() => setSidebarOpen(false)} aria-label="Close menu"><X /></button></div>
        <p className="sidebar-caption">WORKSPACE</p>
        <nav className="dashboard-nav" aria-label="Dashboard navigation">
          {NAV_ITEMS.map(({ label, icon: Icon }) => (
            <button key={label} className={active === label ? "dashboard-nav-item active" : "dashboard-nav-item"} onClick={() => { if (label === "New Diagnosis") { window.location.assign("/new-diagnosis"); return; } setActive(label); setSidebarOpen(false); }}>
              <Icon size={18} strokeWidth={1.8} /><span>{label}</span>
              {label === "New Diagnosis" && <span className="nav-item-plus">+</span>}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-help-icon"><CircleHelp size={18} /></div>
          <div><strong>Need assistance?</strong><span>Explore the system guide</span></div>
          <ArrowUpRight size={15} />
        </div>
        <a href="/" className="back-home-link">← Back to website</a>
      </aside>

      {sidebarOpen && <button className="dashboard-scrim" onClick={() => setSidebarOpen(false)} aria-label="Close sidebar" />}

      <main className="dashboard-main">
        <header className="dashboard-topbar">
          <button className="dashboard-menu" onClick={() => setSidebarOpen(true)} aria-label="Open menu"><Menu /></button>
          <div className="dashboard-breadcrumb"><span>Workspace</span><b>/</b><strong>{active}</strong></div>
          <div className="dashboard-top-actions">
            <button className="dashboard-icon-btn" aria-label="Notifications"><Bell size={18} /><i /></button>
            <div className="dashboard-user"><span className="user-avatar">FS</span><span><strong>FaultSense</strong><small>Project workspace</small></span><ChevronDown size={15} /></div>
          </div>
        </header>

        <div className="dashboard-content">
          <div className="dashboard-welcome">
            <div>
              <p className="dashboard-eyebrow"><span /> INDUSTRIAL MONITORING WORKSPACE</p>
              <h1>{active === "Overview" ? "Welcome to FaultSense AI" : active}</h1>
              <p className="dashboard-intro">Monitor machine conditions and access intelligent fault diagnosis tools.</p>
            </div>
            <div className="dashboard-date-chip"><Activity size={15} /> System workspace</div>
          </div>

          <section className="dashboard-quick-grid" aria-label="Workspace modules">
            <button className="dashboard-module-card featured" onClick={() => window.location.assign("/new-diagnosis")}>
              <span className="module-icon"><PlusCircle size={21} /></span>
              <span className="module-copy"><small>START HERE</small><strong>New Diagnosis</strong><em>Enter machine readings and analyse operating conditions.</em></span>
              <ArrowUpRight className="module-arrow" size={19} />
            </button>
            <button className="dashboard-module-card" onClick={() => setActive("History")}>
              <span className="module-icon"><History size={21} /></span>
              <span className="module-copy"><small>REVIEW</small><strong>Diagnosis History</strong><em>Access previous diagnosis records.</em></span>
              <ArrowUpRight className="module-arrow" size={19} />
            </button>
            <button className="dashboard-module-card" onClick={() => setActive("Rule System")}>
              <span className="module-icon"><GitBranch size={21} /></span>
              <span className="module-copy"><small>KNOWLEDGE</small><strong>Rule System</strong><em>Explore fault rules and diagnostic reasoning.</em></span>
              <ArrowUpRight className="module-arrow" size={19} />
            </button>
          </section>

          <section className="dashboard-panel">
            <div className="dashboard-panel-heading">
              <div><p className="dashboard-eyebrow">INPUT OVERVIEW</p><h2>Machine sensor parameters</h2></div>
              <span className="panel-tag">05 PARAMETERS</span>
            </div>
            <div className="dashboard-input-grid">
              {INPUTS.map(({ label, field, unit, icon: Icon }, index) => (
                <div className="dashboard-input-card" key={field}>
                  <div className="dashboard-input-top"><span className="dashboard-input-icon"><Icon size={18} /></span><span>0{index + 1}</span></div>
                  <strong>{label}</strong><small>{field}</small><em>{unit}</em>
                </div>
              ))}
            </div>
            <p className="dashboard-note">Select <strong>New Diagnosis</strong> from the sidebar to begin. Dashboard modules are presented here as the workspace navigation structure.</p>
          </section>
        </div>
      </main>
    </div>
  );
}
