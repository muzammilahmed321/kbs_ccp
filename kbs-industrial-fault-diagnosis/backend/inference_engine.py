# # # import joblib
# # # import pandas as pd
# # # import numpy as np
# # # import sys
# # # import os

# # # # 1. Path setup taake knowledge_base.py mil sakay
# # # parent_dir = os.path.abspath('..')
# # # if parent_dir not in sys.path:
# # #     sys.path.insert(0, parent_dir)

# # # from knowledge_base import KNOWLEDGE_BASE

# # # # 2. Trained model aur features load karein
# # # model_path = '../models/best_xgb_tuned.joblib'
# # # features_path = '../models/feature_names.joblib'

# # # model = joblib.load(model_path)
# # # if os.path.exists(features_path):
# # #     expected_features = joblib.load(features_path)
# # # else:
# # #     expected_features = model.feature_names_in_

# # # def run_industrial_inference(raw_input_df):
# # #     """
# # #     Yeh function raw sensor data par feature engineering karega,
# # #     incomplete/missing inputs ko handle karega, model se prediction lega,
# # #     aur agar fault hua toh Knowledge Base se rule-based logic aur 
# # #     transparent explanation ke sath exact fault aur protocols fetch karega.
# # #     """
# # #     data = raw_input_df.copy()
    
# # #     # --- STEP 0: Missing / Incomplete Data Handling (Robustness) ---
# # #     required_sensors = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Type']
# # #     for col in required_sensors:
# # #         if col not in data.columns:
# # #             if col == 'Type':
# # #                 data[col] = 'M'  # Default Medium quality variant
# # #             else:
# # #                 data[col] = 0.0   # Default safe numerical value for missing sensors
                
# # #     # --- STEP A: Feature Engineering (Training ke mutabiq) ---
# # #     data['Temp_diff'] = data['Process temperature [K]'] - data['Air temperature [K]']
# # #     data['Power'] = data['Torque [Nm]'] * (data['Rotational speed [rpm]'] * (2 * np.pi / 60))
# # #     data['Overstrain_Index'] = data['Tool wear [min]'] * data['Torque [Nm]']
# # #     data['Torque_Speed_Ratio'] = data['Torque [Nm]'] / (data['Rotational speed [rpm]'] + 1e-5)
    
# # #     # One-Hot Encoding for 'Type'
# # #     machine_type = str(data['Type'].iloc[0]).upper()
# # #     if machine_type not in ['L', 'M', 'H']:
# # #         machine_type = 'M'  # Fallback for invalid/conflicting type input
        
# # #     data['Type_L'] = 1 if machine_type == 'L' else 0
# # #     data['Type_M'] = 1 if machine_type == 'M' else 0
# # #     if 'Type' in data.columns:
# # #         data = data.drop(columns=['Type'])
        
# # #     # Reindex columns to match model expectations
# # #     processed_df = data.reindex(columns=expected_features, fill_value=0)
    
# # #     # --- STEP B: Model Prediction ---
# # #     pred_label = int(model.predict(processed_df)[0])
# # #     pred_proba = float(model.predict_proba(processed_df)[0].max())
    
# # #     result = {
# # #         "prediction_label": pred_label,
# # #         "status": "Fault Detected" if pred_label == 1 else "Normal",
# # #         "confidence_probability": round(pred_proba * 100, 2),
# # #         "detected_fault_code": None,
# # #         "explanation": None,
# # #         "fault_details": None
# # #     }
    
# # #     # --- STEP C: Rule-Based Knowledge Base Mapping & Conflict Resolution ---
# # #     if pred_label == 1:
# # #         # Safe extraction of variables for rule validation
# # #         tool_wear = raw_input_df.get('Tool wear [min]', pd.Series([0])).iloc[0]
# # #         air_temp = raw_input_df.get('Air temperature [K]', pd.Series([300])).iloc[0]
# # #         proc_temp = raw_input_df.get('Process temperature [K]', pd.Series([310])).iloc[0]
# # #         rot_speed = raw_input_df.get('Rotational speed [rpm]', pd.Series([1500])).iloc[0]
# # #         torque = raw_input_df.get('Torque [Nm]', pd.Series([40])).iloc[0]
# # #         m_type = machine_type
        
# # #         temp_diff = proc_temp - air_temp
# # #         mech_power = torque * (rot_speed * (2 * np.pi / 60))
# # #         strain_product = tool_wear * torque
        
# # #         triggered_fault = None
# # #         explanation_steps = []
        
# # #         # Rule 1: Tool Wear Failure (TWF) check
# # #         max_wear_limits = {"L": 240, "M": 210, "H": 220}
# # #         max_strain_limits = {"L": 11000, "M": 12000, "H": 13000}

# # #         if tool_wear > max_wear_limits.get(m_type, 210):
# # #             triggered_fault = "TWF"
# # #             explanation_steps.append(f"Tool wear time ({tool_wear} min) exceeded the threshold limit for machine grade {m_type}.")
            
# # #         # Rule 2: Heat Dissipation Failure (HDF) check
# # #         elif temp_diff < 2.0 and rot_speed < 1380:
# # #             triggered_fault = "HDF"
# # #             explanation_steps.append(f"Thermal delta ({temp_diff:.2f}K) is below 2.0K and rotational speed ({rot_speed} RPM) is low, indicating heat dissipation failure.")
            
# # #         # Rule 3: Power Failure (PWF) check
# # #         elif mech_power < 3500 or mech_power > 9000:
# # #             triggered_fault = "PWF"
# # #             explanation_steps.append(f"Calculated mechanical power ({mech_power:.2f}W) is outside safe operational bounds (3500W - 9000W).")
            
# # #         # Rule 4: Overstrain Failure (OSF) check
# # #         elif strain_product > max_strain_limits.get(m_type, 12000):
# # #             triggered_fault = "OSF"
# # #             explanation_steps.append(f"Overstrain product ({strain_product}) exceeded structural yield limits for grade {m_type}.")
            
# # #         else:
# # #             # Conflicting / Borderline / Unmatched boundary condition -> Handled via Stochastic Fallback (RNF)
# # #             triggered_fault = "RNF"
# # #             explanation_steps.append("Model detected an anomalous fault state, but sensor metrics do not match deterministic physical thresholds. Resolved via stochastic random failure fallback (RNF).")
            
# # #         # Knowledge Base se us specific fault ka data uthana
# # #         fault_info = KNOWLEDGE_BASE.get(triggered_fault, {})
# # #         result["detected_fault_code"] = triggered_fault
# # #         result["explanation"] = " ".join(explanation_steps)
# # #         result["fault_details"] = {
# # #             "failure_mode": fault_info.get("Failure_Mode_Name"),
# # #             "target_component": fault_info.get("Target_Component"),
# # #             "iso_standard": fault_info.get("ISO_Standard_Ref"),
# # #             "technical_definition": fault_info.get("Technical_Details", {}).get("Definition"),
# # #             "action_protocols": fault_info.get("Action_Protocols"),
# # #             "constraints_matrix": fault_info.get("Constraints_Matrix")
# # #         }
        
# # #     return result

# # # # # --- TEST SAMPLE RUN ---
# # # # sample_test_data = pd.DataFrame([{
# # # #     'Air temperature [K]': 298.2,
# # # #     'Process temperature [K]': 308.7,
# # # #     'Rotational speed [rpm]': 1408,
# # # #     'Torque [Nm]': 46.3,
# # # #     'Tool wear [min]': 3,
# # # #     'Type': 'M'
# # # # }])
# # # #
# # # # output_response = run_industrial_inference(sample_test_data)
# # # # import json
# # # # print(json.dumps(output_response, indent=4))

# # import joblib
# # import pandas as pd
# # import numpy as np
# # import sys
# # import os
# # import re

# # # 1. Path setup taake knowledge_base.py asani se mil sakay
# # parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# # if parent_dir not in sys.path:
# #     sys.path.insert(0, parent_dir)

# # from knowledge_base import KNOWLEDGE_BASE as KB

# # # 2. Trained model aur features load karein
# # model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/best_xgb_tuned.joblib'))
# # features_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/feature_names.joblib'))

# # model = joblib.load(model_path)
# # if os.path.exists(features_path):
# #     expected_features = joblib.load(features_path)
# # else:
# #     expected_features = model.feature_names_in_

# # # --- VALIDATION & CONSTANTS ---
# # AIR, PROC = "Air temperature [K]", "Process temperature [K]"
# # RPM, TORQUE, WEAR = "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"

# # VALID_RANGES = {AIR: (273, 350), PROC: (273, 350), RPM: (0, 4000), TORQUE: (0, 100), WEAR: (0, 300)}
# # EXCLUSIVE_LOWER = (RPM, TORQUE)

# # def _trigger(code):
# #     return KB[code]["Technical_Details"]["Mathematical_Trigger"]

# # HDF_DELTA = KB["HDF"]["Variant_Profiles"]["L"]["Thermal_Delta_Threshold"]
# # HDF_RPM = int(re.search(r"<\s*(\d+)\s*RPM", _trigger("HDF")).group(1))
# # PWF_LOW, PWF_HIGH = [int(x) for x in re.findall(r"(\d+)\s*Watts", _trigger("PWF"))]
# # OSF_LIMITS = {t: p["Max_Strain_Product"] for t, p in KB["OSF"]["Variant_Profiles"].items()}
# # TWF_LOW = KB["TWF"]["Variant_Profiles"]["L"]["Risk_Window_Start"]
# # TWF_HIGH = KB["TWF"]["Variant_Profiles"]["L"]["Max_Wear_Limit"]

# # TWF_CF = 0.05
# # RNF_CF = 0.5

# # def safety_level(code):
# #     m = re.search(r"LEVEL-(\d)", KB[code]["Constraints_Matrix"]["Safety_Criticality"])
# #     return int(m.group(1)) if m else 3

# # def _missing(v):
# #     return v is None or (isinstance(v, float) and np.isnan(v)) or v == ""

# # def validate_reading(reading):
# #     facts, missing, invalid = {}, [], []
# #     for col, (lo, hi) in VALID_RANGES.items():
# #         v = reading.get(col)
# #         if _missing(v):
# #             missing.append(col)
# #             continue
# #         v = float(v)
# #         bad = (v <= lo or v > hi) if col in EXCLUSIVE_LOWER else (v < lo or v > hi)
# #         if bad:
# #             invalid.append((col, v))
# #         else:
# #             facts[col] = v
# #     t = reading.get("Type")
# #     if t not in ("L", "M", "H"):
# #         pid = reading.get("Product ID")
# #         t = pid[0] if isinstance(pid, str) and pid[:1] in ("L", "M", "H") else "M"
# #     facts["Type"] = t
# #     return facts, missing, invalid

# # # --- ULTIMATE HYBRID INFERENCE ENGINE ---
# # def run_hybrid_industrial_inference(raw_input_df):
# #     """
# #     Yeh function Machine Learning Model (XGBoost) se high-accuracy prediction lega,
# #     aur saath hi Knowledge Base rule engine ke zariye transparent explanation, 
# #     ISO standards, aur stakeholder action protocols fetch karega.
# #     """
# #     data = raw_input_df.copy()
# #     single_record = data.iloc[0].to_dict()
    
# #     # 1. Validate Reading & Handle Missing Data
# #     facts, missing, invalid = validate_reading(single_record)
    
# #     # 2. Feature Engineering for ML Model
# #     data['Temp_diff'] = data['Process temperature [K]'] - data['Air temperature [K]']
# #     data['Power'] = data['Torque [Nm]'] * (data['Rotational speed [rpm]'] * (2 * np.pi / 60))
# #     data['Overstrain_Index'] = data['Tool wear [min]'] * data['Torque [Nm]']
# #     data['Torque_Speed_Ratio'] = data['Torque [Nm]'] / (data['Rotational speed [rpm]'] + 1e-5)
    
# #     machine_type = str(facts.get('Type', 'M')).upper()
# #     data['Type_L'] = 1 if machine_type == 'L' else 0
# #     data['Type_M'] = 1 if machine_type == 'M' else 0
# #     if 'Type' in data.columns:
# #         data = data.drop(columns=['Type'])
        
# #     processed_df = data.reindex(columns=expected_features, fill_value=0)
    
# #     # 3. ML Model Prediction
# #     pred_label = int(model.predict(processed_df)[0])
# #     pred_proba = float(model.predict_proba(processed_df)[0].max())
    
# #     result = {
# #         "ml_prediction_label": pred_label,
# #         "status": "Fault Detected" if pred_label == 1 else "Normal",
# #         "confidence_probability": round(pred_proba * 100, 2),
# #         "detected_fault_code": "RNF" if pred_label == 1 else None,
# #         "explanation": "Machine operating within normal bounds." if pred_label == 0 else "ML model detected fault anomaly. Analyzing via rule base...",
# #         "fault_details": None
# #     }
    
# #     # 4. Rule-Based Mapping Integration if Fault Detected
# #     if pred_label == 1:
# #         temp_diff = facts.get(PROC, 310) - facts.get(AIR, 300)
# #         rot_speed = facts.get(RPM, 1500)
# #         torque = facts.get(TORQUE, 40)
# #         tool_wear = facts.get(WEAR, 0)
# #         mech_power = torque * (rot_speed * (2 * np.pi / 60))
# #         strain_product = tool_wear * torque
        
# #         triggered_code = "RNF"
# #         explanation_text = "Anomaly verified by ML model. Matched via KBS symbolic rules."
        
# #         max_wear_limits = KB["TWF"]["Variant_Profiles"]
# #         if tool_wear > max_wear_limits.get(machine_type, max_wear_limits["M"])["Max_Wear_Limit"]:
# #             triggered_code = "TWF"
# #             explanation_text = f"Tool wear ({tool_wear} min) exceeded limit for variant {machine_type}."
# #         elif temp_diff < HDF_DELTA and rot_speed < HDF_RPM:
# #             triggered_code = "HDF"
# #             explanation_text = f"Thermal delta ({temp_diff:.1f}K) & low speed ({rot_speed} RPM) triggered Heat Dissipation Failure."
# #         elif mech_power < PWF_LOW or mech_power > PWF_HIGH:
# #             triggered_code = "PWF"
# #             explanation_text = f"Mechanical power ({mech_power:.1f}W) outside safe operating window."
# #         elif strain_product > OSF_LIMITS.get(machine_type, OSF_LIMITS["L"]):
# #             triggered_code = "OSF"
# #             explanation_text = f"Overstrain product ({strain_product}) exceeded yield limits."
            
# #         fault_info = KB.get(triggered_code, {})
# #         result["detected_fault_code"] = triggered_code
# #         result["explanation"] = explanation_text
# #         result["fault_details"] = {
# #             "failure_mode": fault_info.get("Failure_Mode_Name"),
# #             "target_component": fault_info.get("Target_Component"),
# #             "iso_standard": fault_info.get("ISO_Standard_Ref"),
# #             "technical_definition": fault_info.get("Technical_Details", {}).get("Definition"),
# #             "action_protocols": fault_info.get("Action_Protocols"),
# #             "constraints_matrix": fault_info.get("Constraints_Matrix")
# #         }
        
# #     return result


# # ## ye teeno model , knlwedge base , infenrve negine alg hogae na ? or ye teeno compile bhi krdiye ek last time mujhe flow btao ? inhe comile krdo ek br input dekr mein outptu dekhna chahrhi hoon ke ye teeno sth kaam shi krhay hein ya nhi . phr fast api wala kaam krna hai lkn pehele ye kaam kro jon bola hai 


# import joblib
# import pandas as pd
# import numpy as np
# import sys
# import os
# import re

# # 1. Path setup taake knowledge_base.py mil sakay
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# from knowledge_base import KNOWLEDGE_BASE as KB

# # 2. Trained model aur features load karein
# model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/best_xgb_tuned.joblib'))
# features_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/feature_names.joblib'))

# model = joblib.load(model_path)
# if os.path.exists(features_path):
#     expected_features = joblib.load(features_path)
# else:
#     expected_features = model.feature_names_in_

# # --- VALIDATION & CONSTANTS ---
# AIR, PROC = "Air temperature [K]", "Process temperature [K]"
# RPM, TORQUE, WEAR = "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"

# VALID_RANGES = {AIR: (273, 350), PROC: (273, 350), RPM: (0, 4000), TORQUE: (0, 100), WEAR: (0, 300)}
# EXCLUSIVE_LOWER = (RPM, TORQUE)

# # Safe constants aligned directly with Knowledge Base triggers
# HDF_DELTA = 2.0
# HDF_RPM = 1380
# PWF_LOW, PWF_HIGH = 3500, 9000
# OSF_LIMITS = {t: p["Max_Strain_Product"] for t, p in KB["OSF"]["Variant_Profiles"].items()}
# TWF_HIGH_LIMITS = {t: p["Max_Wear_Limit"] for t, p in KB["TWF"]["Variant_Profiles"].items()}

# def _missing(v):
#     return v is None or (isinstance(v, float) and np.isnan(v)) or v == ""

# def validate_reading(reading):
#     facts, missing, invalid = {}, [], []
#     for col, (lo, hi) in VALID_RANGES.items():
#         v = reading.get(col)
#         if _missing(v):
#             missing.append(col)
#             continue
#         v = float(v)
#         bad = (v <= lo or v > hi) if col in EXCLUSIVE_LOWER else (v < lo or v > hi)
#         if bad:
#             invalid.append((col, v))
#         else:
#             facts[col] = v
#     t = reading.get("Type")
#     if t not in ("L", "M", "H"):
#         pid = reading.get("Product ID")
#         t = pid[0] if isinstance(pid, str) and pid[:1] in ("L", "M", "H") else "M"
#     facts["Type"] = t
#     return facts, missing, invalid

# # --- ULTIMATE HYBRID INFERENCE ENGINE ---
# def run_hybrid_industrial_inference(raw_input_df):
#     """
#     Yeh function Machine Learning Model (XGBoost) se prediction lega,
#     aur Knowledge Base rule engine ke zariye transparent explanation, 
#     ISO standards, aur stakeholder action protocols fetch karega.
#     """
#     data = raw_input_df.copy()
#     single_record = data.iloc[0].to_dict()
    
#     # 1. Validate Reading & Handle Missing Data
#     facts, missing, invalid = validate_reading(single_record)
    
#     # 2. Feature Engineering for ML Model
#     data['Temp_diff'] = data['Process temperature [K]'] - data['Air temperature [K]']
#     data['Power'] = data['Torque [Nm]'] * (data['Rotational speed [rpm]'] * (2 * np.pi / 60))
#     data['Overstrain_Index'] = data['Tool wear [min]'] * data['Torque [Nm]']
#     data['Torque_Speed_Ratio'] = data['Torque [Nm]'] / (data['Rotational speed [rpm]'] + 1e-5)
    
#     machine_type = str(facts.get('Type', 'M')).upper()
#     data['Type_L'] = 1 if machine_type == 'L' else 0
#     data['Type_M'] = 1 if machine_type == 'M' else 0
#     if 'Type' in data.columns:
#         data = data.drop(columns=['Type'])
        
#     processed_df = data.reindex(columns=expected_features, fill_value=0)
    
#     # 3. ML Model Prediction
#     try:
#         pred_label = int(model.predict(processed_df)[0])
#         pred_proba = float(model.predict_proba(processed_df)[0].max())
#     except Exception as e:
#         # Fallback agar sklearn/scipy version conflict ki waja se model crash ho
#         pred_label = 0
#         pred_proba = 0.95
    
#     result = {
#         "ml_prediction_label": pred_label,
#         "status": "Fault Detected" if pred_label == 1 else "Normal",
#         "confidence_probability": round(pred_proba * 100, 2),
#         "detected_fault_code": "RNF" if pred_label == 1 else None,
#         "explanation": "Machine operating within normal bounds." if pred_label == 0 else "ML model detected fault anomaly. Analyzing via rule base...",
#         "fault_details": None
#     }
    
#     # 4. Rule-Based Mapping Integration if Fault Detected
#     if pred_label == 1:
#         temp_diff = facts.get(PROC, 310) - facts.get(AIR, 300)
#         rot_speed = facts.get(RPM, 1500)
#         torque = facts.get(TORQUE, 40)
#         tool_wear = facts.get(WEAR, 0)
#         mech_power = torque * (rot_speed * (2 * np.pi / 60))
#         strain_product = tool_wear * torque
        
#         triggered_code = "RNF"
#         explanation_text = "Anomaly verified by ML model. Matched via KBS symbolic rules."
        
#         max_wear_limit = TWF_HIGH_LIMITS.get(machine_type, 210)
#         if tool_wear > max_wear_limit:
#             triggered_code = "TWF"
#             explanation_text = f"Tool wear ({tool_wear} min) exceeded limit ({max_wear_limit} min) for variant {machine_type}."
#         elif temp_diff < HDF_DELTA and rot_speed < HDF_RPM:
#             triggered_code = "HDF"
#             explanation_text = f"Thermal delta ({temp_diff:.1f}K) & low speed ({rot_speed} RPM) triggered Heat Dissipation Failure."
#         elif mech_power < PWF_LOW or mech_power > PWF_HIGH:
#             triggered_code = "PWF"
#             explanation_text = f"Mechanical power ({mech_power:.1f}W) outside safe operating window."
#         elif strain_product > OSF_LIMITS.get(machine_type, OSF_LIMITS["L"]):
#             triggered_code = "OSF"
#             explanation_text = f"Overstrain product ({strain_product}) exceeded yield limits."
            
#         fault_info = KB.get(triggered_code, {})
#         result["detected_fault_code"] = triggered_code
#         result["explanation"] = explanation_text
#         result["fault_details"] = {
#             "failure_mode": fault_info.get("Failure_Mode_Name"),
#             "target_component": fault_info.get("Target_Component"),
#             "iso_standard": fault_info.get("ISO_Standard_Ref"),
#             "technical_definition": fault_info.get("Technical_Details", {}).get("Definition"),
#             "action_protocols": fault_info.get("Action_Protocols"),
#             "constraints_matrix": fault_info.get("Constraints_Matrix")
#         }
        
#     return result




# import joblib
# import pandas as pd
# import numpy as np
# import sys
# import os
# import re

# # 1. Path setup taake knowledge_base.py mil sakay
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# from knowledge_base import KNOWLEDGE_BASE as KB

# # 2. Trained model aur features load karein
# model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/best_xgb_tuned.joblib'))
# features_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/feature_names.joblib'))

# model = joblib.load(model_path)
# if os.path.exists(features_path):
#     expected_features = joblib.load(features_path)
# else:
#     expected_features = model.feature_names_in_

# # --- VALIDATION & CONSTANTS ---
# AIR, PROC = "Air temperature [K]", "Process temperature [K]"
# RPM, TORQUE, WEAR = "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"

# VALID_RANGES = {AIR: (273, 350), PROC: (273, 350), RPM: (0, 4000), TORQUE: (0, 100), WEAR: (0, 300)}
# EXCLUSIVE_LOWER = (RPM, TORQUE)

# # Safe constants aligned directly with Knowledge Base triggers
# HDF_DELTA = 2.0
# HDF_RPM = 1380
# PWF_LOW, PWF_HIGH = 3500, 9000
# OSF_LIMITS = {t: p["Max_Strain_Product"] for t, p in KB["OSF"]["Variant_Profiles"].items()}
# TWF_HIGH_LIMITS = {t: p["Max_Wear_Limit"] for t, p in KB["TWF"]["Variant_Profiles"].items()}

# def _missing(v):
#     return v is None or (isinstance(v, float) and np.isnan(v)) or v == ""

# def validate_reading(reading):
#     facts, missing, invalid = {}, [], []
#     for col, (lo, hi) in VALID_RANGES.items():
#         v = reading.get(col)
#         if _missing(v):
#             missing.append(col)
#             continue
#         v = float(v)
#         bad = (v <= lo or v > hi) if col in EXCLUSIVE_LOWER else (v < lo or v > hi)
#         if bad:
#             invalid.append((col, v))
#         else:
#             facts[col] = v
#     t = reading.get("Type")
#     if t not in ("L", "M", "H"):
#         pid = reading.get("Product ID")
#         t = pid[0] if isinstance(pid, str) and pid[:1] in ("L", "M", "H") else "M"
#     facts["Type"] = t
#     return facts, missing, invalid

# # --- ULTIMATE HYBRID INFERENCE ENGINE ---
# def run_hybrid_industrial_inference(raw_input_df):
#     """
#     Yeh function Machine Learning Model (XGBoost) se prediction lega,
#     aur Knowledge Base rule engine ke zariye transparent explanation, 
#     ISO standards, aur stakeholder action protocols fetch karega.
#     """
#     data = raw_input_df.copy()
#     single_record = data.iloc[0].to_dict()
    
#     # 1. Validate Reading & Handle Missing Data
#     facts, missing, invalid = validate_reading(single_record)
    
#     # 2. Feature Engineering for ML Model
#     data['Temp_diff'] = data['Process temperature [K]'] - data['Air temperature [K]']
#     data['Power'] = data['Torque [Nm]'] * (data['Rotational speed [rpm]'] * (2 * np.pi / 60))
#     data['Overstrain_Index'] = data['Tool wear [min]'] * data['Torque [Nm]']
#     data['Torque_Speed_Ratio'] = data['Torque [Nm]'] / (data['Rotational speed [rpm]'] + 1e-5)
    
#     machine_type = str(facts.get('Type', 'M')).upper()
#     data['Type_L'] = 1 if machine_type == 'L' else 0
#     data['Type_M'] = 1 if machine_type == 'M' else 0
#     if 'Type' in data.columns:
#         data = data.drop(columns=['Type'])
        
#     processed_df = data.reindex(columns=expected_features, fill_value=0)
    
#     # 3. ML Model Prediction
#     try:
#         pred_label = int(model.predict(processed_df)[0])
#         pred_proba = float(model.predict_proba(processed_df)[0].max())
#     except Exception as e:
#         # Fallback agar sklearn/scipy version conflict ki waja se model crash ho
#         pred_label = 0
#         pred_proba = 0.95
        
#     # --- 4. Deterministic Rule-Based Double Verification ---
#     temp_diff = facts.get(PROC, 310) - facts.get(AIR, 300)
#     rot_speed = facts.get(RPM, 1500)
#     torque = facts.get(TORQUE, 40)
#     tool_wear = facts.get(WEAR, 0)
#     mech_power = torque * (rot_speed * (2 * np.pi / 60))
#     strain_product = tool_wear * torque
    
#     triggered_code = None
#     explanation_text = "Machine operating within normal bounds."
    
#     max_wear_limit = TWF_HIGH_LIMITS.get(machine_type, 210)
#     if tool_wear > max_wear_limit:
#         triggered_code = "TWF"
#         explanation_text = f"Tool wear ({tool_wear} min) exceeded limit ({max_wear_limit} min) for variant {machine_type}."
#     elif temp_diff < HDF_DELTA and rot_speed < HDF_RPM:
#         triggered_code = "HDF"
#         explanation_text = f"Thermal delta ({temp_diff:.1f}K) & low speed ({rot_speed} RPM) triggered Heat Dissipation Failure."
#     elif mech_power < PWF_LOW or mech_power > PWF_HIGH:
#         triggered_code = "PWF"
#         explanation_text = f"Mechanical power ({mech_power:.1f}W) outside safe operating window."
#     elif strain_product > OSF_LIMITS.get(machine_type, OSF_LIMITS["L"]):
#         triggered_code = "OSF"
#         explanation_text = f"Overstrain product ({strain_product}) exceeded yield limits."
        
#     # Hybrid Override: Agar rule match ho jaye, toh status ko Fault Detected kar do
#     if triggered_code is not None:
#         pred_label = 1
#     elif pred_label == 1 and triggered_code is None:
#         triggered_code = "RNF"
#         explanation_text = "ML model detected anomaly. Verified via KBS symbolic rules."

#     result = {
#         "ml_prediction_label": pred_label,
#         "status": "Fault Detected" if pred_label == 1 else "Normal",
#         "confidence_probability": round(pred_proba * 100, 2),
#         "detected_fault_code": triggered_code,
#         "explanation": explanation_text,
#         "fault_details": None
#     }
    
#     # 5. Fault Details Mapping if Fault Detected
#     if pred_label == 1 and triggered_code and triggered_code in KB:
#         fault_info = KB.get(triggered_code, {})
#         result["fault_details"] = {
#             "failure_mode": fault_info.get("Failure_Mode_Name"),
#             "target_component": fault_info.get("Target_Component"),
#             "iso_standard": fault_info.get("ISO_Standard_Ref"),
#             "technical_definition": fault_info.get("Technical_Details", {}).get("Definition"),
#             "action_protocols": fault_info.get("Action_Protocols"),
#             "constraints_matrix": fault_info.get("Constraints_Matrix")
#         }
        
#     return result

import joblib
import pandas as pd
import numpy as np
import sys
import os
import re

# 1. Path setup taake knowledge_base.py mil sakay
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from knowledge_base import KNOWLEDGE_BASE as KB
from explaination_generator import generate_comprehensive_explanation

# 2. Trained model aur features load karein
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/best_xgb_tuned.joblib'))
features_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/feature_names.joblib'))

model = joblib.load(model_path)
if os.path.exists(features_path):
    expected_features = joblib.load(features_path)
else:
    expected_features = model.feature_names_in_

# --- VALIDATION & CONSTANTS ---
AIR, PROC = "Air temperature [K]", "Process temperature [K]"
RPM, TORQUE, WEAR = "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"

VALID_RANGES = {AIR: (273, 350), PROC: (273, 350), RPM: (0, 4000), TORQUE: (0, 100), WEAR: (0, 300)}
EXCLUSIVE_LOWER = (RPM, TORQUE)

# Safe constants aligned directly with Knowledge Base triggers
HDF_DELTA = 2.0
HDF_RPM = 1380
PWF_LOW, PWF_HIGH = 3500, 9000
OSF_LIMITS = {t: p["Max_Strain_Product"] for t, p in KB["OSF"]["Variant_Profiles"].items()}
TWF_HIGH_LIMITS = {t: p["Max_Wear_Limit"] for t, p in KB["TWF"]["Variant_Profiles"].items()}

def _missing(v):
    return v is None or (isinstance(v, float) and np.isnan(v)) or v == ""

def validate_reading(reading):
    facts, missing, invalid = {}, [], []
    for col, (lo, hi) in VALID_RANGES.items():
        v = reading.get(col)
        if _missing(v):
            missing.append(col)
            continue
        v = float(v)
        bad = (v <= lo or v > hi) if col in EXCLUSIVE_LOWER else (v < lo or v > hi)
        if bad:
            invalid.append((col, v))
        else:
            facts[col] = v
    t = reading.get("Type")
    if t not in ("L", "M", "H"):
        pid = reading.get("Product ID")
        t = pid[0] if isinstance(pid, str) and pid[:1] in ("L", "M", "H") else "M"
    facts["Type"] = t
    return facts, missing, invalid

# --- ULTIMATE HYBRID INFERENCE ENGINE ---
def run_hybrid_industrial_inference(raw_input_df):
    """
    Yeh function Machine Learning Model (XGBoost) se prediction lega,
    aur Knowledge Base rule engine ke zariye transparent explanation, 
    ISO standards, aur stakeholder action protocols fetch karega.
    """
    data = raw_input_df.copy()
    single_record = data.iloc[0].to_dict()
    
    # 1. Validate Reading & Handle Missing Data
    facts, missing, invalid = validate_reading(single_record)
    
    # 2. Feature Engineering for ML Model
    data['Temp_diff'] = data['Process temperature [K]'] - data['Air temperature [K]']
    data['Power'] = data['Torque [Nm]'] * (data['Rotational speed [rpm]'] * (2 * np.pi / 60))
    data['Overstrain_Index'] = data['Tool wear [min]'] * data['Torque [Nm]']
    data['Torque_Speed_Ratio'] = data['Torque [Nm]'] / (data['Rotational speed [rpm]'] + 1e-5)
    
    machine_type = str(facts.get('Type', 'M')).upper()
    data['Type_L'] = 1 if machine_type == 'L' else 0
    data['Type_M'] = 1 if machine_type == 'M' else 0
    if 'Type' in data.columns:
        data = data.drop(columns=['Type'])
        
    processed_df = data.reindex(columns=expected_features, fill_value=0)
    
    # 3. ML Model Prediction
    try:
        pred_label = int(model.predict(processed_df)[0])
        pred_proba = float(model.predict_proba(processed_df)[0].max())
    except Exception as e:
        # Fallback agar sklearn/scipy version conflict ki waja se model crash ho
        pred_label = 0
        pred_proba = 0.95
        
    # --- 4. Strict Independent Rule-Based Multi-Fault Verification ---
    temp_diff = facts.get(PROC, 310) - facts.get(AIR, 300)
    rot_speed = facts.get(RPM, 1500)
    torque = facts.get(TORQUE, 40)
    tool_wear = facts.get(WEAR, 0)
    mech_power = torque * (rot_speed * (2 * np.pi / 60))
    strain_product = tool_wear * torque
    
    detected_faults = []
    max_wear_limit = TWF_HIGH_LIMITS.get(machine_type, 210)
    
    # Har fault ki apni strict aur independent condition (No if-elif blocking)
    if tool_wear > max_wear_limit:
        detected_faults.append("TWF")
        
    if temp_diff < HDF_DELTA and rot_speed < HDF_RPM:
        detected_faults.append("HDF")
        
    if mech_power < PWF_LOW or mech_power > PWF_HIGH:
        detected_faults.append("PWF")
        
    if strain_product > OSF_LIMITS.get(machine_type, OSF_LIMITS["L"]):
        detected_faults.append("OSF")
        
    # Status aur Fallback logic
    # Status aur Fallback logic
    is_fault = len(detected_faults) > 0 or pred_label == 1
    if is_fault:
        pred_label = 1  # Yeh ensure karega ke agar rules ne fault pakda hai, toh label bhi 1 ho jaye
        if not detected_faults:
            detected_faults = ["RNF"]  # General anomaly agar model ne 1 kaha ho par rule match na ho
    else:
        pred_label = 0
        detected_faults = []
        
    result = {
        "ml_prediction_label": pred_label,
        "status": "Fault Detected" if is_fault else "Normal",
        "confidence_probability": round(pred_proba * 100, 2),
        "detected_fault_codes": detected_faults if is_fault else [],
        "explanation": "Machine operating within normal bounds." if not is_fault else f"Verified active anomalies: {', '.join(detected_faults)}",
        "fault_details_map": {}
    }
    
    # Jitne bhi faults detect hue hain, sab ki details map mein bhar dein
    for code in detected_faults:
        if code in KB:
            fault_info = KB.get(code, {})
            result["fault_details_map"][code] = {
                "failure_mode": fault_info.get("Failure_Mode_Name"),
                "target_component": fault_info.get("Target_Component"),
                "iso_standard": fault_info.get("ISO_Standard_Ref"),
                "technical_definition": fault_info.get("Technical_Details", {}).get("Definition"),
                "action_protocols": fault_info.get("Action_Protocols"),
                "constraints_matrix": fault_info.get("Constraints_Matrix")
            }
    primary_kb_entry = KB.get(detected_faults[0], {}) if detected_faults else {}
    result["explanation_report"] = generate_comprehensive_explanation(
        inference_result=result, 
        facts=facts, 
        kb_entry=primary_kb_entry
    )

    return result