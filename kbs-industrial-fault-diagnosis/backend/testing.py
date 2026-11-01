# import pandas as pd
# import json
# from inference_engine import run_hybrid_industrial_inference

# # All Test Cases (Normal & Faulty Scenarios)
# test_cases = {
#     "1. Normal Machine State": {
#         'Air temperature [K]': 298.2,
#         'Process temperature [K]': 308.7,
#         'Rotational speed [rpm]': 1408,
#         'Torque [Nm]': 46.3,
#         'Tool wear [min]': 3,
#         'Type': 'M'
#     },
#     "2. Tool Wear Failure (TWF)": {
#         'Air temperature [K]': 298.5,
#         'Process temperature [K]': 309.0,
#         'Rotational speed [rpm]': 1400,
#         'Torque [Nm]': 45.0,
#         'Tool wear [min]': 215,  # Medium limit (210) se zyada
#         'Type': 'M'
#     },
#     "3. Heat Dissipation Failure (HDF)": {
#         'Air temperature [K]': 300.0,
#         'Process temperature [K]': 301.0,  # Temp diff = 1.0K (< 2.0K)
#         'Rotational speed [rpm]': 1300,   # Low speed (< 1380 RPM)
#         'Torque [Nm]': 40.0,
#         'Tool wear [min]': 10,
#         'Type': 'L'
#     },
#     "4. Power Failure (PWF)": {
#         'Air temperature [K]': 298.0,
#         'Process temperature [K]': 308.0,
#         'Rotational speed [rpm]': 500,    # Very low speed leading to low power (< 3500W)
#         'Torque [Nm]': 10.0,
#         'Tool wear [min]': 5,
#         'Type': 'H'
#     },
#     "5. Overstrain Failure (OSF)": {
#         'Air temperature [K]': 298.0,
#         'Process temperature [K]': 308.0,
#         'Rotational speed [rpm]': 1500,
#         'Torque [Nm]': 70.0,
#         'Tool wear [min]': 180,  # Strain product = 180 * 70 = 12600 (> 12000 for Medium)
#         'Type': 'M'
#     }
# }

# # Run all test cases sequentially
# for name, data in test_cases.items():
#     print(f"\n==================== RUNNING TEST: {name} ====================")
#     df = pd.DataFrame([data])
#     response = run_hybrid_industrial_inference(df)
#     print(json.dumps(response, indent=4))


import pandas as pd
import json
from inference_engine import run_hybrid_industrial_inference
test_cases = {
    "1. Normal Machine State": {
        'Air temperature [K]': 298.2,
        'Process temperature [K]': 308.7,
        'Rotational speed [rpm]': 1408,
        'Torque [Nm]': 46.3,
        'Tool wear [min]': 3,
        'Type': 'M'
    },
    "2. Tool Wear Failure (TWF)": {
        'Air temperature [K]': 298.5,
        'Process temperature [K]': 309.0,
        'Rotational speed [rpm]': 1400,
        'Torque [Nm]': 45.0,
        'Tool wear [min]': 215,  # Medium limit (210) se zyada
        'Type': 'M'
    },
    "3. Heat Dissipation Failure (HDF)": {
        'Air temperature [K]': 300.0,
        'Process temperature [K]': 301.0,  # Temp diff = 1.0K (< 2.0K)
        'Rotational speed [rpm]': 1300,   # Low speed (< 1380 RPM)
        'Torque [Nm]': 40.0,
        'Tool wear [min]': 10,
        'Type': 'L'
    },
    "4. Power Failure (PWF)": {
        'Air temperature [K]': 298.0,
        'Process temperature [K]': 308.0,
        'Rotational speed [rpm]': 500,    # Very low speed leading to low power (< 3500W)
        'Torque [Nm]': 10.0,
        'Tool wear [min]': 5,
        'Type': 'H'
    },
    "5. Overstrain Failure (OSF)": {
        'Air temperature [K]': 298.0,
        'Process temperature [K]': 308.0,
        'Rotational speed [rpm]': 1500,
        'Torque [Nm]': 70.0,
        'Tool wear [min]': 180,  # Strain product = 180 * 70 = 12600 (> 12000 for Medium)
        'Type': 'M'
    },
    "6. Random / General Noise Failure (RNF)": {
        'Air temperature [K]': 299.0,
        'Process temperature [K]': 308.5,
        'Rotational speed [rpm]': 1450,
        'Torque [Nm]': 42.0,
        'Tool wear [min]': 50,    # Safe limits ke andar, koi strict physical rule match nahi hoga
        'Type': 'M'
    }
}

# Run all test cases sequentially
for name, data in test_cases.items():
    print(f"\n==================== RUNNING TEST: {name} ====================")
    df = pd.DataFrame([data])
    response = run_hybrid_industrial_inference(df)
    print(json.dumps(response, indent=4))
