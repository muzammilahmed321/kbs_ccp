<div align="center">

# ⚙️ FaultSense AI

### Hybrid Symbolic & XGBoost Telemetry Engine for Industrial Equipment Diagnostics

*Real-time fault detection with role-based action protocols for CNC machinery*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Tuned-EC6B23)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?logo=vercel)

**[🚀 Live Demo](https://faultsense-ai.vercel.app/)** · **[🔌 API](https://faultsense-api.vercel.app/)** · **[📖 API Docs](https://faultsense-api.vercel.app/docs)**

</div>

---

## 📌 Table of Contents

[Live Links](#-live-links) · [Overview](#-overview) · [Features](#-features) · [Architecture](#-architecture) · [Fault Modes](#-fault-modes) · [Data Pipeline](#-data-pipeline) · [Model Results](#-model-results) · [Tech Stack](#-tech-stack) · [Project Structure](#-project-structure) · [API](#-api) · [Run Locally](#-run-locally) · [Limitations](#-limitations) · [Future Work](#-future-enhancements) · [Team](#-team)

---

## 🔗 Live Links

| Service | URL |
|---|---|
| 🌐 Frontend | https://faultsense-ai.vercel.app/ |
| ⚡ Backend API | https://faultsense-api.vercel.app/ |
| 📚 Swagger Docs | https://faultsense-api.vercel.app/docs |

---

## 🧭 Overview

Unexpected failures in CNC machinery cause costly downtime and safety hazards. **FaultSense AI** is a web diagnostic portal that takes machine sensor readings and returns an instant, role-specific diagnostic report.

It combines an **XGBoost classifier** with a **symbolic rule engine** backed by a knowledge base. The ML model gives a probability, the rules verify the physics, and the two results are fused into one explained diagnosis.

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🎚️ | **Telemetry Input** | Five sensor readings plus machine quality variant (L / M / H) |
| 🧠 | **Hybrid Inference** | XGBoost probability fused with deterministic rule checks |
| 📚 | **Knowledge-Base Explanations** | ISO references, technical definitions and exact sensor triggers |
| 👷 | **Role-Based Actions** | Separate protocols for Operator, Technician and Manager |
| 🔀 | **Multi-Fault Detection** | Reports concurrent faults, e.g. PWF + OSF |
| 📊 | **Impact Matrix** | Safety level, downtime, cost index and production risk |
| 💾 | **JSON Export** | Download structured diagnostic reports for auditing |

---

## 🏗️ Architecture

```
┌──────────────┐    ┌──────────────────┐    ┌───────────────────────────┐    ┌──────────────────┐
│  Telemetry   │ →  │ FastAPI Backend  │ →  │     Hybrid Inference      │ →  │    Diagnostic    │
│    Input     │    │ validate + feats │    │ XGBoost + Rules + KB      │    │    Dashboard     │
└──────────────┘    └──────────────────┘    └───────────────────────────┘    └──────────────────┘
```

**Workflow**
1. **Input:** the user enters sensor readings and machine variant.
2. **ML prediction:** derived features go to the tuned XGBoost model, which returns a failure probability.
3. **Rule verification:** the knowledge base checks HDF, PWF, OSF and TWF thresholds independently.
4. **Fusion:** verified rules force a "Fault Detected" status. An ML-only alert falls back to RNF.
5. **Explanation:** the generator builds the **What · Why · How Sure · Impact · Action** report.

---

## 🔧 Fault Modes

| Code | Fault | Detection Logic |
|---|---|---|
| **HDF** | Heat Dissipation Failure | Temp difference < 2.0 K **and** speed < 1380 rpm |
| **PWF** | Power Failure | Power < 3500 W **or** > 9000 W |
| **OSF** | Overstrain Failure | Tool wear × Torque > 11000 (L) / 12000 (M) / 13000 (H) |
| **TWF** | Tool Wear Failure | Tool wear > 240 min (L) / 210 min (M) / 220 min (H) |
| **RNF** | Random Failure | ML anomaly flag with no matching rule (fallback) |

**Valid sensor ranges:** Air / Process temperature 273–350 K · Speed 0–4000 rpm · Torque 0–100 Nm · Tool wear 0–300 min

---

## 🔄 Data Pipeline

**Dataset:** AI4I 2020 Predictive Maintenance (Kaggle), about 3% failure rate.

1. **Load & Inspect:** check shape, types, nulls and duplicates.
2. **Explore:** boxplots, histograms, correlation heatmap and failure counts.
3. **Clean & Audit:** drop duplicates, merge repeated UDIs, recover machine type from Product ID, save label mismatches for the rule engine.
4. **Split & Fix:** 80/20 stratified split, invalid readings set to missing, filled with the training median.
5. **Features:** temperature difference, power, overstrain index, torque-speed ratio, one-hot machine type.
6. **Train & Compare:** four models evaluated on the same test set.
7. **Tune & Deploy:** randomized search with 5-fold CV, best XGBoost served via FastAPI.

---

## 📈 Model Results

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC | FP | FN |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Logistic Regression | 0.17 | 0.85 | 0.28 | 0.926 | 0.362 | 287 | 10 |
| Random Forest | 0.62 | 0.74 | 0.67 | 0.972 | 0.773 | 31 | 18 |
| XGBoost (baseline) | 0.83 | 0.78 | 0.80 | 0.949 | 0.830 | 11 | 15 |
| LightGBM | 0.80 | 0.76 | 0.78 | 0.947 | 0.832 | 13 | 16 |
| **XGBoost (tuned)** ✅ | **0.86** | **0.79** | **0.82** | **0.965** | **0.839** | **9** | **14** |

The tuned XGBoost has the best precision, recall, F1 and PR-AUC, and the fewest false alarms and misses.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, lucide-react |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **ML / Data** | XGBoost, scikit-learn, LightGBM, pandas, NumPy, joblib |
| **Deployment** | Vercel (frontend + backend) |

---

## 📁 Project Structure

```
kbs-industrial-fault-diagnosis/
├── main.py                  # FastAPI app (/predict)
├── requirements.txt
├── vercel.json
├── models/                  # tuned XGBoost, scaler, feature names (.joblib)
├── backend/
│   ├── inference_engine.py      # hybrid ML + rules engine
│   ├── knowledge_base.py        # fault knowledge, ISO refs, action matrix
│   ├── explaination_generator.py
│   └── kbs_project_data_pipline (1).ipynb
├── data/                    # raw + processed datasets
├── docs/                    # figures, tables, architecture
└── frontend/                # React + Vite app
    └── src/components/      # Hero, InputPage, DiagnosticResult, ...
```

---

## 🔌 API

**`POST /predict`**

```json
{
  "air_temperature": 300,
  "process_temperature": 310,
  "rotational_speed": 1500,
  "torque": 40,
  "tool_wear": 100,
  "machine_type": "L"
}
```

**Response:** `{ "status": "success", "prediction_result": { status, confidence_probability, detected_fault_codes, fault_details_map, explanation_report } }`

**`GET /`** returns a health message. Full interactive docs are at [`/docs`](https://faultsense-api.vercel.app/docs).

---

## 💻 Run Locally

**Backend** (from the project root)
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
cp .env.example .env        # VITE_API_BASE_URL=http://127.0.0.1:8000
npm install
npm run dev
```

---

## ⚠️ Limitations

- Trained on one synthetic dataset (AI4I 2020), not real plant data.
- Covers five fault modes. RNF is a fallback label, not a physical fault.
- Manual sensor entry only, with no PLC / SCADA / IoT link.
- About 79% recall, so some real failures can be missed.
- Rule thresholds are manually set and not calibrated on real machines.
- No database or login. Records are kept through JSON export.

## 🚀 Future Enhancements

1. Live PLC / IoT sensor integration
2. Validation on real industrial data and threshold calibration
3. SHAP-based feature explanations
4. Maintenance history database with role-based login
5. Remaining Useful Life prediction

---

## 👥 Team

**NED University of Engineering & Technology**
Department of Computer Science & Information Technology · BS Artificial Intelligence · Batch 2024–2028

**Course:** Knowledge Base System  ·  **Instructor:** Miss Meher

| Name | Roll Number |
|---|---|
| Izma Warsia | CT-24311 |
| Safa Khurram | CT-24310 |
| M. Muzammil Ahmed Qureshi | CT-24307 |
| Habib Ur Rehman | CT-24080 |
| Daniyal Hussain | CT-24093 |

---

<div align="center">

Made for the Knowledge Base System course project, November 2026

</div>
