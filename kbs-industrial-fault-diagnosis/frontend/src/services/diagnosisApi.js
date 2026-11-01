const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

/** Call this from the New Diagnosis form when the user clicks Run Diagnostics. */
export async function runDiagnosis(sensorReadings, selectedRole = "Operator") {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      air_temperature: Number(sensorReadings.air_temperature),
      process_temperature: Number(sensorReadings.process_temperature),
      rotational_speed: Number(sensorReadings.rotational_speed),
      torque: Number(sensorReadings.torque),
      tool_wear: Number(sensorReadings.tool_wear),
      machine_type: sensorReadings.machine_type,
    }),
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = typeof payload.detail === "string" ? payload.detail : `API request failed (${response.status})`;
    throw new Error(detail);
  }

  // FastAPI returns { status: "success", prediction_result: {...} }.
  const prediction = payload.prediction_result ?? payload;
  if (!prediction || !prediction.status || !prediction.explanation_report) {
    throw new Error("API response format unexpected. Check the /predict response.");
  }

  const saved = {
    ...prediction,
    // Keep the exact readings submitted by the operator beside the backend result.
    sensor_readings: {
      air_temperature: Number(sensorReadings.air_temperature),
      process_temperature: Number(sensorReadings.process_temperature),
      rotational_speed: Number(sensorReadings.rotational_speed),
      torque: Number(sensorReadings.torque),
      tool_wear: Number(sensorReadings.tool_wear),
      machine_type: sensorReadings.machine_type,
    },
    selected_role: selectedRole,
    received_at: new Date().toISOString(),
  };
  sessionStorage.setItem("faultsense_diagnostic_result", JSON.stringify(saved));
  window.location.assign("/diagnosis-result");
  return saved;
}
