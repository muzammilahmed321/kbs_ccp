# FaultSense AI – UI update notes

The frontend now has three routed pages:

- `/` – existing landing page (kept intact)
- `/new-diagnosis` – compact sensor input page with five readings, stakeholder selection and machine quality selection
- `/diagnosis-result` – structured diagnostic report rendered from the live `/predict` FastAPI response

The old dashboard route is no longer part of the user flow. Landing-page calls to action now open the sensor input page.

The result page reads `status`, `confidence_probability`, `detected_fault_codes`, `fault_details_map`, `explanation_report`, and the submitted sensor readings from the response saved by `diagnosisApi.js`. Fault details and impact cards are data-driven, so single-fault and multi-fault responses (for example HDF, PWF, and PWF + OSF) are supported without hardcoded case selection. Normal responses show a separate no-fault state.

## Run locally

Frontend: `cd frontend && npm install && npm run dev`

Backend: from the project root, install `requirements.txt`, then run `uvicorn main:app --reload` (the frontend defaults to `http://127.0.0.1:8000`; override with `VITE_API_BASE_URL` if needed).

The input page is designed to fit on one desktop screen at common laptop/desktop sizes. On narrow/mobile screens, normal vertical scrolling is retained for accessibility.
