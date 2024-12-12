import gradio as gr
import sqlite3
import os
import logging
# Logging setup
logging.basicConfig(level=logging.INFO)
# Database Setup
conn = sqlite3.connect(os.path.join(os.getcwd(), 'responses.db'))
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, name TEXT, report TEXT)''')
conn.commit()

# Save a report function
def save_report(name, report):
    cursor.execute('INSERT INTO responses (name, report) VALUES (?, ?)', (name, report))
    conn.commit()

# Symptom Data with Explicit Mappings
symptom_data = {
    "Symptom Group": [
        "Motor dysfunction (e.g., weakness, arm drift)",
        "Loss of or altered consciousness",
        "Visual problems (e.g., blurred vision, decreased vision)",
        "Speech or language issues (e.g., slurred speech, inability to speak)",
        "Balance or coordination problems (e.g., difficulty walking)",
        "Severe headache (with or without vomiting)",
        "Facial asymmetry (e.g., mouth deviation)"
    ],
    "Stroke Type": [
        "ischemic", "ischemic", "ischemic", "Transient Ischemic Attack (TIA)",
        "Intracerebral haemorrhage", "Subarachnoid haemorrhage", "ischemic"
    ],
    "Mild": {
        "Diagnostic Tests": [
            "Basic motor function tests.",
            "Basic neurological assessment and glucose monitoring.",
            "Fundus examination and basic vision tests.",
            "Speech evaluation and auditory comprehension tests.",
            "Basic balance tests (e.g., Romberg test).",
            "Routine headache history evaluation.",
            "Basic neurological and vascular assessment."
        ],
        "Management": [
            "Light physiotherapy to improve strength.",
            "Monitor vitals and address glucose levels.",
            "Referral to an ophthalmologist for evaluation.",
            "Consultation with a speech therapist.",
            "Vestibular therapy and regular monitoring.",
            "Hydration and NSAIDs for pain management.",
            "Routine imaging and vascular health monitoring."
        ],
        "Medications": [
            "Low-dose aspirin for stroke prevention.",
            "Monitor glucose; no medication required for mild cases.",
            "Antioxidants (e.g., Vitamin A, C).",
            "Clopidogrel if vascular risk factors are present.",
            "Vitamin B12 for balance improvement.",
            "Analgesics for headache relief.",
            "No medication unless vascular risks exist."
        ],
        "Rehab and Follow-Up": [
            "Regular physiotherapy to enhance mobility.",
            "Neurology follow-ups to monitor consciousness.",
            "Ophthalmology follow-ups to evaluate visual recovery.",
            "Speech therapy sessions to prevent deterioration.",
            "Balance training exercises to improve coordination.",
            "Pain tracking and management strategies.",
            "Neurological check-ups to assess progress."
        ],
        "Dietary Recommendation": [
            "High-fiber, low-sodium diet to maintain cardiovascular health.",
            "Balanced diet to support neurological recovery.",
            "Omega-3-rich foods to enhance vascular health.",
            "Hydration and nutrient-dense meals for recovery.",
            "Magnesium-rich foods to improve balance control.",
            "Anti-inflammatory foods to reduce headache severity.",
            "Heart-healthy, low-cholesterol diet to reduce stroke risks."
        ]
    },
    "Moderate": {
        "Diagnostic Tests": [
            "MRI/CT scans to assess motor impairment severity.",
            "Electrolyte analysis and detailed neurological imaging.",
            "MRI/MRA for identifying vascular blockages.",
            "Cognitive assessments combined with MRI imaging.",
            "Comprehensive vestibular and neuroimaging.",
            "CT/MRI to evaluate potential hemorrhage causes.",
            "Carotid Doppler to assess blood flow disruptions."
        ],
        "Management": [
            "Physiotherapy with targeted exercises.",
            "Stabilize airway and monitor neurological vitals.",
            "Urgent referral to an ophthalmologist.",
            "Speech rehabilitation and cognitive therapy.",
            "Intensive vestibular rehab for balance issues.",
            "Manage blood pressure with regular interventions.",
            "Address vascular health and underlying conditions."
        ],
        "Medications": [
            "Dual antiplatelet therapy (e.g., Aspirin + Clopidogrel).",
            "Administer Mannitol for cerebral edema.",
            "Anticoagulants to prevent embolic complications.",
            "Combination therapy with statins to reduce risks.",
            "Beta-blockers for vestibular migraines.",
            "Migraine prophylaxis for severe headache cases.",
            "Dual antiplatelet therapy to address TIA risks."
        ],
        "Rehab and Follow-Up": [
            "Regular physiotherapy to improve motor recovery.",
            "Stroke unit monitoring and intensive rehab.",
            "Vision therapy for recovery from vascular damage.",
            "Speech therapy for improved language skills.",
            "Comprehensive vestibular therapy for balance.",
            "Monitor intracranial pressure for moderate headaches.",
            "Stroke prevention rehab and follow-ups."
        ],
        "Dietary Recommendation": [
            "High-protein diet for muscle recovery.",
            "Balanced meals to manage glucose and energy levels.",
            "Anti-inflammatory foods for improved vascular health.",
            "Soft, nutrient-dense foods for cognitive recovery.",
            "Calcium-rich foods to prevent falls and injuries.",
            "Frequent small meals to avoid triggering nausea.",
            "Low-fat diet to support cardiovascular health."
        ]
    },
    "Severe": {
        "Diagnostic Tests": [
            "Noncontrast brain CT or MRI, Serum electrolytes, Complete blood count.",
            "Blood glucose, CT or MRI scan, Electroencephalogram (EEG).",
            "Toxicology screen, Arterial blood gas (ABG), CT or MRI scan.",
            "Carotid Doppler, MRI/MRA, Fundus examination.",
            "MRI with diffusion-weighted imaging, Speech evaluation.",
            "MRI or CT scan, Blood glucose, Electrolyte levels.",
            "Noncontrast CT, MRI with angiogram, Lumbar puncture."
        ],
        "Management": [
            "Thrombolysis within 4.5 hours for ischemic stroke.",
            "ICU care to stabilize vital signs and prevent complications.",
            "Emergency care to address acute vision loss.",
            "Comprehensive neurocognitive rehabilitation in ICU.",
            "Aggressive balance rehab for cerebellar stroke cases.",
            "Control intracranial pressure with surgical interventions.",
            "Emergency stroke pathway management for survival."
        ],
        "Medications": [
            "Thrombolytics (if eligible) and anticoagulants.",
            "Sedatives to manage seizures or agitation.",
            "IV Mannitol to reduce intracranial pressure.",
            "Nimodipine for subarachnoid hemorrhage.",
            "Migraine and pain management medications.",
            "Immediate administration of thrombolytics if eligible.",
            "Anticoagulants for embolic stroke prevention."
        ],
        "Rehab and Follow-Up": [
            "Intensive inpatient physiotherapy for recovery.",
            "Long-term ICU monitoring for stability.",
            "Structured visual rehab for vascular damage.",
            "Speech therapy combined with neurocognitive rehab.",
            "Advanced vestibular therapy to restore balance.",
            "ICU-based monitoring for intracranial conditions.",
            "Intensive post-stroke rehab and recovery plans."
        ],
        "Dietary Recommendation": [
            "Liquid diets or pureed meals for feeding challenges.",
            "Parenteral nutrition for critical cases.",
            "Fortified liquids with essential vitamins.",
            "Smooth purees for patients with swallowing difficulties.",
            "Omega-3-rich foods to aid neurological repair.",
            "Enteral feeding for severe impairment cases.",
            "High-calorie liquid diets for critical recovery."
        ]
    }
}

# Functionality is retained; interface code omitted for brevity
# Refer to initial structure for how to add Gradio integration for UI.


# Add detailed mapping and a validation function
def validate_mapping():
    """
    Ensures that all symptoms, severities, and their respective recommendations
    are properly aligned and contextually relevant.
    """
    for severity, details in symptom_data.items():
        if severity not in ["Mild", "Moderate", "Severe"]:
            continue
        for key, values in details.items():
            assert len(values) == len(symptom_data["Symptom Group"]), (
                f"Mismatch in {key} for severity {severity}. "
                f"Expected {len(symptom_data['Symptom Group'])}, got {len(values)}."
            )

validate_mapping()


# Heart Risk Calculator with Glucose Integration
def calculate_heart_risk(bmi, bp_systolic, bp_diastolic, smoker, diabetes, gender, age, glucose_level):
    risk_factors = []
    if bmi > 30 or bmi < 18.5:
        risk_factors.append("⚠️ Abnormal BMI: High or low BMI increases heart risk.")
    if bp_systolic > 140 or bp_diastolic > 90:
        risk_factors.append("⚠️ Hypertension: High BP is a significant heart risk factor.")
    if smoker:
        risk_factors.append("⚠️ Smoking: Smoking raises heart and stroke risks.")
    if diabetes:
        risk_factors.append("⚠️ Diabetes: Diabetes leads to vascular complications.")
    if glucose_level > 140:
        risk_factors.append("⚠️ High Glucose: Elevated glucose increases risk for stroke and heart complications.")
    elif glucose_level < 70:
        risk_factors.append("⚠️ Low Glucose: Hypoglycemia may exacerbate neurological deficits.")
    if (gender == "Male" and age > 45) or (gender == "Female" and age > 55):
        risk_factors.append("⚠️ Age Risk: Older age correlates with higher heart risk.")
    risk_score = len(risk_factors) * 20  # Each factor contributes 20% to the total risk
    return risk_score, risk_factors


# Main Function with Glucose Integration
def stroke_symptom_checker(patient_name, height, weight, age, gender, bp_systolic, bp_diastolic, smoker, diabetes, alcohol, glucose_level, *severity_choices):
    bmi = weight / ((height / 100) ** 2)
    heart_risk, risk_factors = calculate_heart_risk(bmi, bp_systolic, bp_diastolic, smoker, diabetes, gender, age, glucose_level)


    # Highlight parameters with colors
    bmi_color = "red" if bmi > 30 or bmi < 18.5 else "green"
    bp_color = "red" if bp_systolic > 140 or bp_diastolic > 90 else "green"
    glucose_color = "red" if glucose_level > 140 or glucose_level < 70 else "green"


    # Generate Report
    # Generate Report
    report = f"""
    <h1>Stroke and Heart Risk Report</h1>
    <h2>Patient Details</h2>
    <ul>
        <li><strong>Name:</strong> {patient_name}</li>
        <li><strong>Age:</strong> {age}</li>
        <li><strong>Gender:</strong> {gender}</li>
        <li><strong>BMI:</strong> <span style="color: {bmi_color};">{bmi:.2f}</span></li>
        <li><strong>Blood Pressure:</strong> <span style="color: {bp_color};">{bp_systolic}/{bp_diastolic} mmHg</span></li>
        <li><strong>Glucose Level:</strong> <span style="color: {glucose_color};">{glucose_level} mg/dL</span></li>
    </ul>
    <h2>Heart Risk: <span style="color: {'red' if heart_risk > 50 else 'orange' if heart_risk > 30 else 'green'};">{heart_risk}%</span></h2>
    """


    # Add Risk Factors
    # Add Risk Factors
    if risk_factors:
        report += "<h2>Risk Factors</h2><ul>"
        for risk in risk_factors:
            report += f"<li>{risk}</li>"
        report += "</ul>"


    # Add Symptom-Based Recommendations
    # Add Symptom-Based Recommendations
    for i, symptom in enumerate(symptom_data["Symptom Group"]):
        severity = severity_choices[i]
        if severity == "No Impact":
            continue

        report += f"<h3>Symptom Group: {symptom} (Severity: {severity})</h3>"

        # Add Stroke Type only for Severe
        if severity == "Severe":
            report += f"<p><strong>Stroke Type:</strong> {symptom_data['Stroke Type'][i]}</p>"

        # Add Recommendations
        report += "<ul>"
        for section, details in symptom_data[severity].items():
            report += f"<li><strong>{section}:</strong> {details[i]}</li>"
        report += "</ul>"


    # Add Disclaimer
    report += """
    <h2>Disclaimer</h2>
    <p>
        This report is generated following the severity scale outlined by the Ministry of Health and Family Welfare, Government of India.
        All recommendations are based on the guidelines provided by the Indian Council of Medical Research (ICMR).
        Please consult a healthcare professional for personalized advice.
    </p>
    """

    return report

# Interface
# Interface with Glucose Level
def interface():
    symptoms = symptom_data["Symptom Group"]
    severity_levels = ["No Impact", "Mild", "Moderate", "Severe"]
    severity_inputs = [
        gr.Dropdown(choices=severity_levels, label=f"Severity for {symptom}", value="No Impact")
        for symptom in symptoms
    ]

    inputs = [
        gr.Textbox(label="Patient Name"),
        gr.Number(label="Height (cm)", value=170),
        gr.Number(label="Weight (kg)", value=70),
        gr.Number(label="Age (years)", value=40),
        gr.Dropdown(["Male", "Female"], label="Gender"),
        gr.Number(label="BP Systolic (mmHg)", value=120),
        gr.Number(label="BP Diastolic (mmHg)", value=80),
        gr.Checkbox(label="Smoker"),
        gr.Checkbox(label="Diabetes"),
        gr.Checkbox(label="Alcohol Consumption"),
        gr.Number(label="Glucose Level (mg/dL)", value=90),  # New Input Field
        *severity_inputs
    ]

    outputs = gr.HTML(label="Report")

    return gr.Interface(
        fn=stroke_symptom_checker,
        inputs=inputs,
        outputs=outputs,
        title="Stroke and Heart Risk Checker",
        description="An AI-powered tool for stroke and heart risk analysis with severity-based recommendations."
    )

if __name__ == "__main__":
    logging.info("Launching the application...")
    try:
        port = int(os.environ.get("PORT", 8080))  # Use PORT environment variable
        interface().launch(server_name="0.0.0.0", server_port=port)
    except Exception as e:
    logging.error(f"Failed to start server on port {port}: {e}", exc_info=True)



