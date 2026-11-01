def generate_comprehensive_explanation(inference_result, facts, kb_entry):
    """
    Turns an inference-engine result into plain text addressing:
    1. WHAT was found
    2. WHY (Which rule and exact sensor values)
    3. HOW SURE the system is (Confidence probability)
    4. WHAT THE IMPACT IS (Downtime & Financial risk)
    5. WHAT TO DO (Action protocols)
    """
    fault_codes = inference_result.get("detected_fault_codes", [])
    is_normal = inference_result.get("status") == "Normal"
    confidence = inference_result.get("confidence_probability", 0.0)
    
    if is_normal or not fault_codes:
        return {
            "summary_card": "Machine status is Normal. All telemetry and operational parameters are within ISO tolerances.",
            "what": "No anomalies or active failure modes detected.",
            "why": f"Evaluated sensor readings (Air Temp: {facts.get('Air temperature [K]}')}K, Process Temp: {facts.get('Process temperature [K]}')}K, Torque: {facts.get('Torque [Nm]}')}Nm, Wear: {facts.get('Tool wear [min]}')}min) comply safely with physical threshold limits.",
            "how_sure": f"Model Confidence: {confidence}% (Normal operational baseline).",
            "impact": "Zero downtime impact. 100% equipment availability maintained.",
            "action": "Continue standard scheduled monitoring. No intervention required."
        }

    # Agar koi fault detect hua hai (Multiple faults support ke sath)
    primary_code = fault_codes[0] # Primary fault focus
    fault_name = kb_entry.get("Failure_Mode_Name", primary_code)
    target_comp = kb_entry.get("Target_Component", "CNC Subsystem")
    action_protos = kb_entry.get("Action_Protocols", {})
    constraints = kb_entry.get("Constraints_Matrix", {})

    # 1. WHAT was found
    what_text = f"Active Fault Mode(s) Detected: {', '.join(fault_codes)} ({fault_name}) affecting the {target_comp}."

    # 2. WHY it happened (Contextual metrics based on fault type)
    if primary_code == "TWF":
        why_text = f"Rule Triggered: Tool wear duration exceeded safe limits for variant {facts.get('Type')}. Recorded wear: {facts.get('Tool wear [min]}')} mins."
    elif primary_code == "HDF":
        why_text = f"Rule Triggered: Critical thermal differential (< 2.0K) combined with low spindle speed (< 1380 RPM). Recorded speed: {facts.get('Rotational speed [rpm]}')} RPM."
    elif primary_code == "PWF":
        why_text = f"Rule Triggered: Mechanical power output fell outside safe window (< 3500W or > 9000W) due to extreme torque-speed ratios."
    elif primary_code == "OSF":
        why_text = f"Rule Triggered: Cumulative strain product (Tool Wear $\times$ Torque) exceeded structural yield yield limits for variant {facts.get('Type')}."
    else:
        why_text = f"Rule Triggered: General anomaly / statistical noise pattern identified by ML model telemetry analysis."

    # 3. HOW SURE
    how_sure_text = f"System Diagnostic Confidence: {confidence}% (Cross-verified via hybrid symbolic rule engine and XGBoost model)."

    # 4. IMPACT
    downtime = constraints.get('Downtime_Impact', 'Standard operational delay.')
    financial = constraints.get('Financial_Cost_Index', 'Moderate resource cost.')
    safety = constraints.get('Safety_Criticality', 'Standard plant safety protocol.')
    impact_text = f"Operational Impact — Downtime: {downtime} | Financial Risk: {financial} | Safety Level: {safety}"

    # 5. WHAT TO DO (Action Protocols)
    operator_action = action_protos.get('Floor_Operator_Action', 'Halt machine immediately.')
    technician_action = action_protos.get('Maintenance_Technician_Action', 'Inspect component parameters.')
    manager_action = action_protos.get('Plant_Manager_Action', 'Review production schedule.')
    
    action_text = (
        f"Recommended Action Protocols -> "
        f"[Operator]: {operator_action} | "
        f"[Technician]: {technician_action} | "
        f"[Manager]: {manager_action}"
    )

    # Master plain-text narrative combining everything smoothly
    master_summary = (
        f"DIAGNOSTIC REPORT: {what_text} "
        f"{why_text} {how_sure_text} {impact_text} "
        f"Immediate Protocol: {operator_action}"
    )

    return {
        "summary_card": master_summary,
        "what": what_text,
        "why": why_text,
        "how_sure": how_sure_text,
        "impact": impact_text,
        "action": action_text
    }