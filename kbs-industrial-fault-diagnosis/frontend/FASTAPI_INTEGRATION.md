# Connect the New Diagnosis form to FastAPI

The result page now reads the actual response saved by `runDiagnosis()`; it no longer selects hardcoded HDF/PWF/OSF preview cases.

## 1. Configure the API URL

Copy `.env.example` to `.env` and set:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart Vite after changing `.env`.

## 2. Call the API from the form's Run Diagnostics handler

In the component that owns the sensor input form:

```jsx
import { runDiagnosis } from "../services/diagnosisApi";

const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

async function handleRunDiagnostics() {
  setLoading(true);
  setError("");
  try {
    await runDiagnosis({
      air_temperature: form.air_temperature,
      process_temperature: form.process_temperature,
      rotational_speed: form.rotational_speed,
      torque: form.torque,
      tool_wear: form.tool_wear,
      machine_type: form.machine_type, // expected machine type, e.g. L / M / H per backend
    }, selectedRole); // "Operator", "Technician", or "Manager"
    // runDiagnosis saves the real prediction_result and navigates to /diagnosis-result
  } catch (err) {
    setError(err.message || "Unable to run diagnosis.");
  } finally {
    setLoading(false);
  }
}
```

Attach `onClick={handleRunDiagnostics}` to the Run Diagnostics button and show `error` near the form. Disable the button while `loading` is true.

## 3. Start the backend and frontend

Backend (from the folder containing `main.py`):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
npm install
npm run dev
```

Open the frontend URL, submit the form, and it will POST JSON to `POST /predict`. The helper unwraps `{ "status": "success", "prediction_result": {...} }` and stores the prediction for the result route.

## Expected request keys

`air_temperature`, `process_temperature`, `rotational_speed`, `torque`, `tool_wear`, `machine_type`.

The browser and FastAPI must be reachable from the same machine/network. If hosted separately, set `VITE_API_BASE_URL` to the backend's reachable URL and configure FastAPI CORS for the frontend origin.
