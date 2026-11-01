import { useMemo, useState } from "react";
import { Activity, AlertTriangle, BadgeCheck, CheckCircle2, Download, Gauge, RotateCcw, ShieldAlert, Wrench, Zap, Clock3, Factory } from "lucide-react";

const ROLE_OPTIONS = [
  { label: "Floor Operator", key: "Floor_Operator_Action" },
  { label: "Maintenance Technician", key: "Maintenance_Technician_Action" },
  { label: "Plant Manager", key: "Plant_Manager_Action" },
];
const ROLE_ALIASES = {
  "Floor Operator": "Floor Operator", "Operator": "Floor Operator",
  "Maintenance Tech": "Maintenance Technician", "Maintenance Technician": "Maintenance Technician", "Technician": "Maintenance Technician",
  "Plant Manager": "Plant Manager", "Manager": "Plant Manager"
};
const IMPACT_FIELDS = [
  { key: "Safety_Criticality", label: "Safety criticality", icon: ShieldAlert },
  { key: "Downtime_Impact", label: "Downtime", icon: Clock3 },
  { key: "Financial_Cost_Index", label: "Financial cost", icon: Gauge },
  { key: "Production_Continuity", label: "Production continuity", icon: Factory },
];

function confidence(value) {
  const n = Number(value);
  return Number.isFinite(n) ? `${Number(n.toFixed(2))}%` : "Not provided";
}
function textOr(value, fallback = "Not provided by the backend") {
  return value === undefined || value === null || value === "" ? fallback : String(value);
}
function severity(text = "") {
  const match = String(text).match(/LEVEL-(\d)/i);
  return match ? Number(match[1]) : 0;
}
function stripBackendHeading(value, headingPattern) {
  const raw = textOr(value, "");
  return raw.replace(headingPattern, "").trim();
}

function explanationSections(report, isFault) {
  const sections = [];
  const add = (heading, content) => {
    const value = textOr(content, "").trim();
    if (value) sections.push({ heading, content: value });
  };

  if (isFault) {
    // Fault names, impact and action protocols have dedicated sections below.
    // Keep this panel focused on the backend's actual diagnostic reasoning.
    add("Rule Triggered", stripBackendHeading(report.why, /^Rule Triggered:\s*/i));
    add("System Diagnostic Confidence", stripBackendHeading(report.how_sure, /^System Diagnostic Confidence:\s*/i));
  } else {
    add("Normal Operating Assessment", report.what);
    add("Sensor Evaluation", report.why);
    add("System Diagnostic Confidence", stripBackendHeading(report.how_sure, /^Model Confidence:\s*/i));
  }
  return sections;
}

export default function DiagnosticResult() {
  const [storedResult] = useState(() => {
    try { return JSON.parse(sessionStorage.getItem("faultsense_diagnostic_result") || "null"); }
    catch { return null; }
  });
  const result = storedResult;
  const [role, setRole] = useState(() => ROLE_ALIASES[storedResult?.selected_role] || "Floor Operator");

  const faults = useMemo(() => Object.entries(result?.fault_details_map || {}), [result]);
  const codes = result?.detected_fault_codes?.length ? result.detected_fault_codes : faults.map(([code]) => code);
  const isFault = result?.status === "Fault Detected" || codes.length > 0;
  const report = result?.explanation_report || {};
  const highestSafety = Math.max(0, ...faults.map(([, fault]) => severity(fault.constraints_matrix?.Safety_Criticality)));

  const reset = () => { window.location.assign("/new-diagnosis"); };
  const exportReport = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `FaultSense-${(codes.join("-") || "NORMAL")}-diagnostic.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  if (!result) return <main className="diagnostic-page output-v2"><header className="output-topbar"><a href="/" className="output-brand"><Activity/> FAULTSENSE <b>AI</b></a></header><section className="output-empty"><AlertTriangle/><h1>No diagnostic result yet</h1><p>Submit your five sensor readings to display the response returned by the backend.</p><a href="/new-diagnosis" className="output-primary">Open sensor input</a></section></main>;

  return <main className="diagnostic-page output-v2">
    <header className="output-topbar"><a href="/" className="output-brand"><span><Activity size={18}/></span> FAULTSENSE <b>AI</b></a><div className="output-top-actions"><span className="output-live-dot"/> LIVE BACKEND RESULT</div></header>
    <div className="output-container">
      <div className="output-page-heading"><div><div className="output-kicker">DIAGNOSTIC REPORT</div><h1>Machine <em>diagnosis</em></h1><p>Hybrid AI + rule-engine assessment from your submitted sensor readings.</p></div><div className="output-confidence"><strong>{confidence(result.confidence_probability)}</strong><span>MODEL CONFIDENCE</span><small className={`output-ai-prediction ${isFault ? "fault" : "normal"}`}>AI PREDICTION {isFault ? "FAULT" : "NORMAL"}</small></div></div>

      <section className={`output-status ${isFault ? "has-fault" : "is-normal"}`}>
        <div className="output-status-icon">{isFault ? <AlertTriangle size={23}/> : <CheckCircle2 size={23}/>}</div>
        <div className="output-status-copy"><span className="output-status-label">{isFault ? "Fault Detected" : "Normal"}</span><h2>{isFault ? `${codes.length} ${codes.length === 1 ? "fault mode" : "fault modes"} identified` : "Machine operating within normal limits"}</h2></div>
      </section>

      {isFault ? <section className="output-fault-section"><div className="output-section-heading"><div><span>01 / FAULT IDENTIFICATION</span><h2>Detected failure mode{faults.length > 1 ? "s" : ""}</h2></div><small>{codes.join(" + ")}</small></div>
        <div className={`output-fault-grid count-${Math.min(faults.length, 3)}`}>{faults.map(([code, fault]) => <article className="output-fault-card" key={code}>
          <div className="output-fault-heading"><div className="output-fault-code">{code}</div><div className="output-fault-name"><h3>{textOr(fault.failure_mode, code)}</h3><span>{textOr(fault.iso_standard)}</span></div></div>
          <div className="output-target"><small>AFFECTED COMPONENT</small><p>{textOr(fault.target_component)}</p></div>
          <div className="output-definition"><small>TECHNICAL DEFINITION</small><p>{textOr(fault.technical_definition)}</p></div>
        </article>)}</div>
      </section> : <section className="output-normal-note"><CheckCircle2/><div><h2>No active fault codes</h2><p>No active fault codes were returned by the backend. The machine is operating within the evaluated normal limits.</p></div></section>}

      <section className="output-impact-section"><div className="output-section-heading"><div><span>02 / OPERATIONAL CONSEQUENCES</span><h2>Impact assessment</h2></div><small>{highestSafety ? `HIGHEST SAFETY LEVEL ${highestSafety}` : "NO FAULT RISK REPORTED"}</small></div>
        {isFault ? <div className="output-impact-grid">{faults.map(([code, fault]) => <div className="output-impact-group" key={code}><div className="output-impact-code">{code} <span>{textOr(fault.failure_mode, "")}</span></div><div className="output-impact-cards">{IMPACT_FIELDS.map(field => { const Icon = field.icon; return <article className="output-impact-card" key={field.key}><span className="output-impact-icon"><Icon size={15}/></span><small>{field.label}</small><p>{textOr(fault.constraints_matrix?.[field.key])}</p></article>; })}</div></div>)}</div> : <div className="output-impact-grid"><div className="output-impact-cards output-normal-impact"><article className="output-impact-card"><span className="output-impact-icon"><Clock3 size={15}/></span><small>OPERATIONAL IMPACT</small><p>{textOr(report.impact, "Zero downtime impact reported.")}</p></article><article className="output-impact-card"><span className="output-impact-icon"><Wrench size={15}/></span><small>RECOMMENDED ACTION</small><p>{textOr(report.action, "Continue standard scheduled monitoring.")}</p></article></div></div>}
      </section>

      <section className="output-explanation-section"><div className="output-section-heading"><div><span>03 / AI REASONING</span><h2>Why this result?</h2></div><small><BadgeCheck size={14}/> BACKEND EXPLANATION</small></div>
        <div className="output-explanation-card"><div className="output-explanation-mark"><Zap size={18}/></div><div className="output-explanation-body">
          {explanationSections(report, isFault).map((section, index) => <section key={`${section.heading}-${index}`}><h3>{section.heading}</h3>{section.items ? <div className="output-explanation-impact-list">{section.items.map((item, itemIndex) => <p key={`${item.heading}-${itemIndex}`}>{item.heading && <strong>{item.heading}: </strong>}{item.content}</p>)}</div> : <p>{section.content}</p>}</section>)}
        </div></div>
      </section>

      <section className="output-stakeholder-section"><div className="output-section-heading"><div><span>04 / RESPONSE PLAN</span><h2>Stakeholder action</h2></div><div className="output-role-picker"><span>VIEW AS</span><div className="output-role-tabs">{ROLE_OPTIONS.map(option => <button type="button" key={option.label} className={role === option.label ? "active" : ""} onClick={() => setRole(option.label)}>{option.label}</button>)}</div></div></div>
        {isFault ? <div className="output-action-list">{faults.map(([code, fault]) => <article className="output-action-card output-action-card-expanded" key={code}><div className="output-action-code">{code}</div><div className="output-action-content"><h3>{textOr(fault.failure_mode, code)}</h3><div className="output-stakeholder-actions">{ROLE_OPTIONS.map(option => <section className={`output-stakeholder-action ${role === option.label ? "selected" : ""}`} key={option.key}><strong>{option.label}</strong><p>{textOr(fault.action_protocols?.[option.key], "No role-specific action was supplied in the backend response.")}</p></section>)}</div></div></article>)}</div> : <div className="output-normal-note output-action-normal"><CheckCircle2/><div><h2>No intervention required</h2><p>{textOr(report.action, "Continue standard scheduled monitoring.")}</p></div></div>}
        <p className="output-safety-note"><ShieldAlert size={14}/> Follow your facility's approved safety, isolation and lockout procedures. High-voltage and machine interventions must be handled by qualified personnel.</p>
      </section>

      <footer className="output-footer"><span>FAULTSENSE AI <b>·</b> INDUSTRIAL DIAGNOSTICS</span><div><button type="button" className="output-secondary" onClick={reset}><RotateCcw size={14}/> Run another diagnosis</button><button type="button" className="output-primary" onClick={exportReport}><Download size={14}/> Export backend result</button></div></footer>
    </div>
  </main>;
}
