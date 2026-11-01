import { useState } from "react";
import { Activity, Check, Cpu, Gauge, LoaderCircle, RotateCcw, ShieldCheck, Thermometer, Wrench, Zap, ArrowRight, Minus, Plus } from "lucide-react";
import { runDiagnosis } from "../services/diagnosisApi.js";

const initial = { air_temperature: 298.2, process_temperature: 308.6, rotational_speed: 1500, torque: 40, tool_wear: 100 };
const roles = [
  { id: "Floor Operator", title: "Floor Operator", note: "Operations" },
  { id: "Maintenance Tech", title: "Maintenance Technician", note: "Engineering" },
  { id: "Plant Manager", title: "Plant Manager", note: "Management" },
];
const fields = [
  { key: "air_temperature", title: "Air temperature", unit: "K", min: 273, max: 350, step: .1, icon: Thermometer },
  { key: "process_temperature", title: "Process temperature", unit: "K", min: 273, max: 350, step: .1, icon: Thermometer },
  { key: "rotational_speed", title: "Rotational speed", unit: "RPM", min: 0, max: 4000, step: 1, icon: Gauge },
  { key: "torque", title: "Torque load", unit: "Nm", min: 0, max: 100, step: .1, icon: Zap },
  { key: "tool_wear", title: "Tool wear", unit: "min", min: 0, max: 300, step: 1, icon: Wrench },
];

export default function InputPage() {
  const [role, setRole] = useState("Floor Operator");
  const [machineType, setMachineType] = useState("M");
  const [values, setValues] = useState(initial);
  const [loading, setLoading] = useState(false);
  const [dialDragging, setDialDragging] = useState(false);
  const [error, setError] = useState("");
  const update = (key, value) => setValues(current => ({ ...current, [key]: value }));
  const updateDial = event => {
    if (!dialDragging && event.type !== "pointerdown") return;
    const rect = event.currentTarget.getBoundingClientRect();
    const angle = Math.atan2(event.clientY - (rect.top + rect.height / 2), event.clientX - (rect.left + rect.width / 2)) * 180 / Math.PI;
    const fraction = ((angle + 90 + 360) % 360) / 360;
    update("tool_wear", Math.round(fraction * 300));
  };
  const applyPreset = preset => {
    if (preset === "baseline") setValues(initial);
    if (preset === "fault") setValues({ ...initial, rotational_speed: 500, torque: 40, tool_wear: 100 });
    if (preset === "highwear") setValues({ ...initial, rotational_speed: 500, torque: 65, tool_wear: 200, process_temperature: 315.2 });
    setError("");
  };
  const submit = async event => {
    event.preventDefault();
    setError("");
    const invalid = fields.find(field => values[field.key] === "" || !Number.isFinite(Number(values[field.key])) || Number(values[field.key]) < field.min || Number(values[field.key]) > field.max);
    if (invalid) { setError(`${invalid.title} must be between ${invalid.min} and ${invalid.max} ${invalid.unit}.`); return; }
    setLoading(true);
    try {
      const readings = Object.fromEntries(fields.map(field => [field.key, Number(values[field.key])]));
      await runDiagnosis({ ...readings, machine_type: machineType }, role);
    } catch (err) {
      setError(err.message || "Unable to connect to the diagnosis service.");
      setLoading(false);
    }
  };

  return <main className="diagnosis-input-page input-v2">
    <div className="di-shell">
      <header className="di-topbar">
        <a href="/" className="di-brand"><span className="di-brand-icon"><Cpu size={18}/></span><span>FAULTSENSE <b>AI</b></span></a>
        <div className="di-top-right"><a href="/" className="di-back">Home</a><span className="di-online"><i/> FASTAPI CONNECTED</span></div>
      </header>
      <section className="di-heading di-heading-compact">
        <div><div className="di-kicker"><span/> SENSOR CONFIGURATION</div><h1>Machine <em>Inputs</em></h1><p>Enter the current machine readings and select the report audience.</p></div>
        
      </section>
      <form onSubmit={submit} className="di-form di-form-compact">
        <section className="di-context-compact">
          <div className="di-context-group di-stakeholder-centered"><div className="di-mini-label">STAKEHOLDER VIEW</div><div className="di-role-grid di-role-grid-compact">{roles.map(item => <button type="button" key={item.id} onClick={() => setRole(item.id)} className={`di-role ${role === item.id ? "selected" : ""}`}><span className="di-role-copy"><strong>{item.title}</strong><small>{item.note}</small></span><span className="di-radio">{role === item.id && <Check size={11}/>}</span></button>)}</div></div>
          <div className="di-context-group di-machine-compact di-machine-centered"><div className="di-mini-label">MACHINE QUALITY</div><div className="di-type-options">{[{id:"L",name:"Low"},{id:"M",name:"Medium"},{id:"H",name:"High"}].map(type => <button type="button" key={type.id} onClick={() => setMachineType(type.id)} className={machineType === type.id ? "active" : ""}><b>{type.id}</b><small>{type.name}</small></button>)}</div></div>
        </section>
        <section className="di-sensors di-sensors-compact">
          <div className="di-section-head di-section-head-compact"><div><span className="di-step">01</span><div><h2>Sensor readings</h2><p>All five parameters are required for the diagnosis.</p></div></div><span className="di-section-meta">5 INPUTS</span></div>
          <div className="di-sensor-grid di-sensor-grid-compact">{fields.map((field, index) => { const Icon = field.icon; return <article className="di-sensor-card di-sensor-card-compact" key={field.key}>
            <div className="di-sensor-card-head"><span className="di-sensor-icon"><Icon size={16}/></span><span className="di-sensor-index">0{index + 1}</span></div>
            <label htmlFor={field.key}>{field.title}</label>
            <div className="di-value-line"><input id={field.key} type="number" min={field.min} max={field.max} step={field.step} value={values[field.key]} onChange={event => update(field.key, event.target.value)} required/><span>{field.unit}</span></div>
            {index < 2 ? <><input className="di-range" aria-label={`${field.title} slider`} type="range" min={field.min} max={field.max} step={field.step} value={values[field.key] === "" ? field.min : values[field.key]} onChange={event => update(field.key, event.target.value)}/><div className="di-range-bounds"><span>{field.min}</span><span>{field.max}</span></div></> : index < 4 ? <div className="di-stepper"><button type="button" aria-label={`Decrease ${field.title}`} onClick={() => update(field.key, Number(Math.max(field.min, Number(values[field.key]) - field.step).toFixed(field.step < 1 ? 1 : 0)))}><Minus size={14}/></button><span>Adjust value</span><button type="button" aria-label={`Increase ${field.title}`} onClick={() => update(field.key, Number(Math.min(field.max, Number(values[field.key]) + field.step).toFixed(field.step < 1 ? 1 : 0)))}><Plus size={14}/></button></div> : <div className="di-dial-wrap"><div className="di-dial" style={{ background: `conic-gradient(from 0deg, #70dfba ${Number(values[field.key]) / 300 * 100}%, rgba(255,255,255,.12) 0)` }} role="slider" aria-label={`${field.title} rotary control`} aria-valuemin={field.min} aria-valuemax={field.max} aria-valuenow={Number(values[field.key])} tabIndex={0} onPointerDown={event => { setDialDragging(true); event.currentTarget.setPointerCapture(event.pointerId); updateDial(event); }} onPointerMove={updateDial} onPointerUp={() => setDialDragging(false)} onPointerCancel={() => setDialDragging(false)} onKeyDown={event => { if (event.key === "ArrowUp" || event.key === "ArrowRight") update(field.key, Math.min(field.max, Number(values[field.key]) + 1)); if (event.key === "ArrowDown" || event.key === "ArrowLeft") update(field.key, Math.max(field.min, Number(values[field.key]) - 1)); }}><div className="di-dial-center"><strong>{values[field.key]}</strong><small>TURN TO ADJUST</small></div></div></div>}
          </article>; })}</div>
          <div className="di-presets di-presets-compact"><span>QUICK VALUES</span><button type="button" onClick={() => applyPreset("baseline")}>Normal test</button><button type="button" onClick={() => applyPreset("fault")}>Single-fault test</button><button type="button" onClick={() => applyPreset("highwear")}>Combined-fault test</button><button type="button" className="di-reset" onClick={() => { setValues(initial); setError(""); }}><RotateCcw size={12}/> Reset</button></div>
        </section>
        <div className="di-submit-row di-submit-row-compact"><div className="di-assurance"><ShieldCheck size={18}/><span><strong>Ready for analysis</strong><small>Readings are sent to the live hybrid inference API.</small></span></div><button className="di-submit" type="submit" disabled={loading}>{loading ? <><LoaderCircle className="di-spin" size={17}/> ANALYSING</> : <>RUN DIAGNOSTICS <ArrowRight size={17}/></>}</button></div>
        {error && <div className="di-error" role="alert">{error}</div>}
      </form>
      <footer className="di-footer"><span>FAULTSENSE AI <b>·</b> INDUSTRIAL DIAGNOSTICS</span></footer>
    </div>
  </main>;
}
