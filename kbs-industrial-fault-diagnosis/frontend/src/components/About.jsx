import { BrainCircuit, Database, GitBranch, ClipboardCheck, ArrowRight } from "lucide-react";

const STAGES = [
  {
    icon: BrainCircuit,
    tag: "MACHINE LEARNING",
    title: "XGBoost prediction",
    detail: "Estimates whether the machine may be heading towards failure.",
  },
  {
    icon: Database,
    tag: "KNOWLEDGE BASE",
    title: "Fault knowledge",
    detail: "Stores fault symptoms, thresholds, variants and action protocols.",
  },
  {
    icon: GitBranch,
    tag: "REASONING",
    title: "Inference engine",
    detail: "Applies production rules to connect evidence with a diagnosis.",
  },
  {
    icon: ClipboardCheck,
    tag: "DECISION SUPPORT",
    title: "Diagnosis report",
    detail: "Presents the identified fault, reasoning and maintenance guidance.",
  },
];

export default function About() {
  return (
    <section id="about" className="section about-section combined-about-section">
      <div className="container">
        <div className="about-unified-heading">
          <p className="eyebrow">ABOUT FAULTSENSE AI</p>
          <h2>Understand the machine.<br /><span className="accent">Act before failure.</span></h2>
          <p className="lead">
            FaultSense AI combines machine-learning predictions with a knowledge-based
            reasoning system to diagnose potential milling-machine faults and support
            maintenance decisions.
          </p>
        </div>

        <div className="architecture-panel">
          <div className="architecture-topline">
            <span><span className="signal-live-dot" /> OUR DIAGNOSTIC APPROACH</span>
            <span className="architecture-caption">FROM PREDICTION TO EXPLAINABLE ACTION</span>
          </div>

          <div className="architecture-flow about-architecture-flow">
            {STAGES.map(({ icon: Icon, tag, title, detail }, index) => (
              <div className="architecture-stage" key={title}>
                <div className="architecture-stage-head">
                  <span className="architecture-stage-icon"><Icon size={25} strokeWidth={1.7} /></span>
                  <span className="architecture-stage-number">0{index + 1}</span>
                </div>
                <span className="architecture-stage-tag">{tag}</span>
                <h3>{title}</h3>
                <p>{detail}</p>
                {index < STAGES.length - 1 && <ArrowRight className="architecture-stage-arrow" size={19} />}
              </div>
            ))}
          </div>

          <div className="architecture-bottomline">
            <span>ML PREDICTION</span><span>•</span>
            <span>FAULT KNOWLEDGE</span><span>•</span>
            <span>RULE-BASED REASONING</span><span>•</span>
            <span>MAINTENANCE SUPPORT</span>
          </div>
        </div>
      </div>
    </section>
  );
}
