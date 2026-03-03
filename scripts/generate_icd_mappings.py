"""
Generate ICD Mappings and Critical Conditions from AGBonnet Dataset
====================================================================

This script:
1. Downloads AGBonnet/augmented-clinical-notes dataset
2. Analyzes full_note and summary fields
3. Extracts medical conditions
4. Maps to ICD-10 codes
5. Generates icd_mapping.json and critical_condition.json
"""

import json
import re
from collections import Counter
from datasets import load_dataset
import pandas as pd

print("="*80)
print("DOWNLOADING AND ANALYZING AGBonnet DATASET")
print("="*80)

# Load dataset
print("\nLoading dataset...")
dataset = load_dataset("AGBonnet/augmented-clinical-notes", split="train")
print(f"Loaded {len(dataset)} clinical records")

# Analyze a sample
print("\nAnalyzing dataset structure...")
sample = dataset[0]
print(f"Available columns: {dataset.column_names}")
print(f"\nSample full_note length: {len(sample['full_note'])} chars")

# Extract conditions from multiple records
print("\n" + "="*80)
print("EXTRACTING MEDICAL CONDITIONS")
print("="*80)

# Medical condition patterns (comprehensive)
condition_patterns = {
    # Cardiovascular
    'myocardial_infarction': r'\b(myocardial infarction|MI|heart attack|STEMI|NSTEMI)\b',
    'heart_failure': r'\b(heart failure|cardiac failure|congestive heart failure|CHF)\b',
    'hypertension': r'\b(hypertension|high blood pressure|HTN)\b',
    'atrial_fibrillation': r'\b(atrial fibrillation|AF|AFib)\b',
    'coronary_artery_disease': r'\b(coronary artery disease|CAD|coronary heart disease)\b',
    'cardiac_arrest': r'\b(cardiac arrest|cardiopulmonary arrest)\b',
    'stroke': r'\b(stroke|cerebrovascular accident|CVA|brain attack)\b',
    'pulmonary_embolism': r'\b(pulmonary embolism|PE)\b',

    # Respiratory
    'pneumonia': r'\b(pneumonia|lung infection)\b',
    'copd': r'\b(COPD|chronic obstructive pulmonary disease|emphysema|chronic bronchitis)\b',
    'asthma': r'\b(asthma|bronchial asthma)\b',
    'respiratory_failure': r'\b(respiratory failure|acute respiratory distress)\b',
    'tuberculosis': r'\b(tuberculosis|TB)\b',

    # Endocrine
    'diabetes_mellitus': r'\b(diabetes mellitus|diabetes|DM)\b',
    'type_1_diabetes': r'\b(type 1 diabetes|T1DM|insulin-dependent diabetes)\b',
    'type_2_diabetes': r'\b(type 2 diabetes|T2DM|non-insulin-dependent diabetes)\b',
    'diabetic_ketoacidosis': r'\b(diabetic ketoacidosis|DKA)\b',
    'hyperthyroidism': r'\b(hyperthyroidism|thyrotoxicosis)\b',
    'hypothyroidism': r'\b(hypothyroidism)\b',

    # Infectious
    'sepsis': r'\b(sepsis|septicemia|blood infection)\b',
    'septic_shock': r'\b(septic shock)\b',
    'meningitis': r'\b(meningitis)\b',
    'encephalitis': r'\b(encephalitis)\b',

    # Neurological
    'epilepsy': r'\b(epilepsy|seizure disorder)\b',
    'seizure': r'\b(seizure|convulsion)\b',
    'parkinsons_disease': r'\b(Parkinson\'s disease|parkinsonism)\b',
    'alzheimers_disease': r'\b(Alzheimer\'s disease|dementia)\b',
    'multiple_sclerosis': r'\b(multiple sclerosis|MS)\b',

    # Psychiatric
    'bipolar_disorder': r'\b(bipolar disorder|bipolar affective disorder|manic depression)\b',
    'major_depression': r'\b(major depression|major depressive disorder|MDD|clinical depression)\b',
    'schizophrenia': r'\b(schizophrenia|psychosis)\b',
    'anxiety_disorder': r'\b(anxiety disorder|generalized anxiety)\b',

    # Renal
    'chronic_kidney_disease': r'\b(chronic kidney disease|CKD|chronic renal failure)\b',
    'acute_kidney_injury': r'\b(acute kidney injury|AKI|acute renal failure)\b',

    # Hepatic
    'cirrhosis': r'\b(cirrhosis|liver cirrhosis)\b',
    'hepatitis': r'\b(hepatitis)\b',
    'liver_failure': r'\b(liver failure|hepatic failure)\b',

    # Cancer
    'lung_cancer': r'\b(lung cancer|pulmonary carcinoma)\b',
    'breast_cancer': r'\b(breast cancer|mammary carcinoma)\b',
    'colon_cancer': r'\b(colon cancer|colorectal cancer)\b',
    'leukemia': r'\b(leukemia|leukaemia)\b',
    'lymphoma': r'\b(lymphoma)\b',

    # GI
    'peptic_ulcer': r'\b(peptic ulcer|gastric ulcer|duodenal ulcer)\b',
    'pancreatitis': r'\b(pancreatitis)\b',
    'appendicitis': r'\b(appendicitis)\b',
    'cholecystitis': r'\b(cholecystitis)\b',

    # Other
    'anemia': r'\b(anemia|anaemia)\b',
    'fracture': r'\b(fracture|broken bone)\b',
    'osteoporosis': r'\b(osteoporosis)\b',
    'rheumatoid_arthritis': r'\b(rheumatoid arthritis|RA)\b',
}

# Scan dataset
total_records = len(dataset)
print(f"\nScanning ALL {total_records} records for conditions...")
condition_counts = Counter()

for i in range(total_records):
    if i % 1000 == 0:
        print(f"  Processed {i}/{total_records} records ({i*100//total_records}%)...", end='\r')

    full_note = dataset[i]['full_note'].lower()

    for condition_name, pattern in condition_patterns.items():
        if re.search(pattern, full_note, re.IGNORECASE):
            condition_counts[condition_name] += 1

print(f"\nProcessed {total_records} records")
print(f"\nFound {len(condition_counts)} distinct conditions")
print("\nTop 20 most common conditions:")
for condition, count in condition_counts.most_common(20):
    print(f"  {condition}: {count} occurrences")

# Generate ICD-10 mappings
print("\n" + "="*80)
print("GENERATING ICD-10 MAPPINGS")
print("="*80)

icd_mapping = {
    # Cardiovascular
    "myocardial_infarction": {
        "icd10_code": "I21.9",
        "description": "Acute myocardial infarction, unspecified",
        "category": "cardiovascular",
        "severity": "critical"
    },
    "heart_failure": {
        "icd10_code": "I50.9",
        "description": "Heart failure, unspecified",
        "category": "cardiovascular",
        "severity": "severe"
    },
    "hypertension": {
        "icd10_code": "I10",
        "description": "Essential (primary) hypertension",
        "category": "cardiovascular",
        "severity": "moderate"
    },
    "atrial_fibrillation": {
        "icd10_code": "I48.91",
        "description": "Unspecified atrial fibrillation",
        "category": "cardiovascular",
        "severity": "moderate"
    },
    "coronary_artery_disease": {
        "icd10_code": "I25.10",
        "description": "Atherosclerotic heart disease of native coronary artery",
        "category": "cardiovascular",
        "severity": "severe"
    },
    "cardiac_arrest": {
        "icd10_code": "I46.9",
        "description": "Cardiac arrest, cause unspecified",
        "category": "cardiovascular",
        "severity": "critical"
    },
    "stroke": {
        "icd10_code": "I63.9",
        "description": "Cerebral infarction, unspecified",
        "category": "cardiovascular",
        "severity": "critical"
    },
    "pulmonary_embolism": {
        "icd10_code": "I26.99",
        "description": "Other pulmonary embolism without acute cor pulmonale",
        "category": "cardiovascular",
        "severity": "critical"
    },

    # Respiratory
    "pneumonia": {
        "icd10_code": "J18.9",
        "description": "Pneumonia, unspecified organism",
        "category": "respiratory",
        "severity": "severe"
    },
    "copd": {
        "icd10_code": "J44.9",
        "description": "Chronic obstructive pulmonary disease, unspecified",
        "category": "respiratory",
        "severity": "severe"
    },
    "asthma": {
        "icd10_code": "J45.909",
        "description": "Unspecified asthma, uncomplicated",
        "category": "respiratory",
        "severity": "moderate"
    },
    "respiratory_failure": {
        "icd10_code": "J96.90",
        "description": "Respiratory failure, unspecified",
        "category": "respiratory",
        "severity": "critical"
    },
    "tuberculosis": {
        "icd10_code": "A15.9",
        "description": "Respiratory tuberculosis unspecified",
        "category": "infectious",
        "severity": "severe"
    },

    # Endocrine
    "diabetes_mellitus": {
        "icd10_code": "E11.9",
        "description": "Type 2 diabetes mellitus without complications",
        "category": "endocrine",
        "severity": "moderate"
    },
    "type_1_diabetes": {
        "icd10_code": "E10.9",
        "description": "Type 1 diabetes mellitus without complications",
        "category": "endocrine",
        "severity": "moderate"
    },
    "type_2_diabetes": {
        "icd10_code": "E11.9",
        "description": "Type 2 diabetes mellitus without complications",
        "category": "endocrine",
        "severity": "moderate"
    },
    "diabetic_ketoacidosis": {
        "icd10_code": "E10.10",
        "description": "Type 1 diabetes mellitus with ketoacidosis",
        "category": "endocrine",
        "severity": "critical"
    },
    "hyperthyroidism": {
        "icd10_code": "E05.90",
        "description": "Thyrotoxicosis, unspecified",
        "category": "endocrine",
        "severity": "moderate"
    },
    "hypothyroidism": {
        "icd10_code": "E03.9",
        "description": "Hypothyroidism, unspecified",
        "category": "endocrine",
        "severity": "mild"
    },

    # Infectious
    "sepsis": {
        "icd10_code": "A41.9",
        "description": "Sepsis, unspecified organism",
        "category": "infectious",
        "severity": "critical"
    },
    "septic_shock": {
        "icd10_code": "R65.21",
        "description": "Severe sepsis with septic shock",
        "category": "infectious",
        "severity": "critical"
    },
    "meningitis": {
        "icd10_code": "G03.9",
        "description": "Meningitis, unspecified",
        "category": "infectious",
        "severity": "critical"
    },
    "encephalitis": {
        "icd10_code": "G04.90",
        "description": "Encephalitis, unspecified",
        "category": "infectious",
        "severity": "critical"
    },

    # Neurological
    "epilepsy": {
        "icd10_code": "G40.909",
        "description": "Epilepsy, unspecified, not intractable",
        "category": "neurological",
        "severity": "moderate"
    },
    "seizure": {
        "icd10_code": "R56.9",
        "description": "Unspecified convulsions",
        "category": "neurological",
        "severity": "severe"
    },
    "parkinsons_disease": {
        "icd10_code": "G20",
        "description": "Parkinson's disease",
        "category": "neurological",
        "severity": "severe"
    },
    "alzheimers_disease": {
        "icd10_code": "G30.9",
        "description": "Alzheimer's disease, unspecified",
        "category": "neurological",
        "severity": "severe"
    },
    "multiple_sclerosis": {
        "icd10_code": "G35",
        "description": "Multiple sclerosis",
        "category": "neurological",
        "severity": "severe"
    },

    # Psychiatric
    "bipolar_disorder": {
        "icd10_code": "F31.9",
        "description": "Bipolar disorder, unspecified",
        "category": "psychiatric",
        "severity": "moderate"
    },
    "major_depression": {
        "icd10_code": "F32.9",
        "description": "Major depressive disorder, single episode, unspecified",
        "category": "psychiatric",
        "severity": "moderate"
    },
    "schizophrenia": {
        "icd10_code": "F20.9",
        "description": "Schizophrenia, unspecified",
        "category": "psychiatric",
        "severity": "severe"
    },
    "anxiety_disorder": {
        "icd10_code": "F41.9",
        "description": "Anxiety disorder, unspecified",
        "category": "psychiatric",
        "severity": "mild"
    },

    # Renal
    "chronic_kidney_disease": {
        "icd10_code": "N18.9",
        "description": "Chronic kidney disease, unspecified",
        "category": "renal",
        "severity": "severe"
    },
    "acute_kidney_injury": {
        "icd10_code": "N17.9",
        "description": "Acute kidney failure, unspecified",
        "category": "renal",
        "severity": "critical"
    },

    # Hepatic
    "cirrhosis": {
        "icd10_code": "K74.60",
        "description": "Unspecified cirrhosis of liver",
        "category": "hepatic",
        "severity": "severe"
    },
    "hepatitis": {
        "icd10_code": "K75.9",
        "description": "Inflammatory liver disease, unspecified",
        "category": "hepatic",
        "severity": "moderate"
    },
    "liver_failure": {
        "icd10_code": "K72.90",
        "description": "Hepatic failure, unspecified",
        "category": "hepatic",
        "severity": "critical"
    },

    # Cancer
    "lung_cancer": {
        "icd10_code": "C34.90",
        "description": "Malignant neoplasm of unspecified part of unspecified bronchus or lung",
        "category": "oncology",
        "severity": "critical"
    },
    "breast_cancer": {
        "icd10_code": "C50.919",
        "description": "Malignant neoplasm of unspecified site of unspecified female breast",
        "category": "oncology",
        "severity": "critical"
    },
    "colon_cancer": {
        "icd10_code": "C18.9",
        "description": "Malignant neoplasm of colon, unspecified",
        "category": "oncology",
        "severity": "critical"
    },
    "leukemia": {
        "icd10_code": "C95.90",
        "description": "Leukemia, unspecified",
        "category": "oncology",
        "severity": "critical"
    },
    "lymphoma": {
        "icd10_code": "C85.90",
        "description": "Non-Hodgkin lymphoma, unspecified",
        "category": "oncology",
        "severity": "critical"
    },

    # GI
    "peptic_ulcer": {
        "icd10_code": "K27.9",
        "description": "Peptic ulcer, site unspecified",
        "category": "gastrointestinal",
        "severity": "moderate"
    },
    "pancreatitis": {
        "icd10_code": "K85.90",
        "description": "Acute pancreatitis, unspecified",
        "category": "gastrointestinal",
        "severity": "severe"
    },
    "appendicitis": {
        "icd10_code": "K35.80",
        "description": "Unspecified acute appendicitis",
        "category": "gastrointestinal",
        "severity": "severe"
    },
    "cholecystitis": {
        "icd10_code": "K81.9",
        "description": "Cholecystitis, unspecified",
        "category": "gastrointestinal",
        "severity": "moderate"
    },

    # Other
    "anemia": {
        "icd10_code": "D64.9",
        "description": "Anemia, unspecified",
        "category": "hematological",
        "severity": "mild"
    },
    "fracture": {
        "icd10_code": "S02.9XXA",
        "description": "Unspecified fracture of skull",
        "category": "trauma",
        "severity": "moderate"
    },
    "osteoporosis": {
        "icd10_code": "M81.0",
        "description": "Age-related osteoporosis without current pathological fracture",
        "category": "musculoskeletal",
        "severity": "moderate"
    },
    "rheumatoid_arthritis": {
        "icd10_code": "M06.9",
        "description": "Rheumatoid arthritis, unspecified",
        "category": "musculoskeletal",
        "severity": "moderate"
    }
}

# Add occurrence counts to mapping
for condition, data in icd_mapping.items():
    data['occurrences_in_dataset'] = condition_counts.get(condition, 0)

print(f"\nGenerated ICD-10 mappings for {len(icd_mapping)} conditions")

# Generate critical conditions
print("\n" + "="*80)
print("GENERATING CRITICAL CONDITIONS")
print("="*80)

critical_conditions = {}
for condition, data in icd_mapping.items():
    if data['severity'] == 'critical':
        critical_conditions[condition] = {
            "icd10_code": data['icd10_code'],
            "description": data['description'],
            "category": data['category'],
            "severity": "critical",
            "requires_immediate_intervention": True,
            "mortality_risk": "high",
            "typical_onset": "acute",
            "occurrences_in_dataset": data['occurrences_in_dataset']
        }

print(f"\nIdentified {len(critical_conditions)} critical conditions")
print("\nCritical conditions:")
for condition in critical_conditions:
    print(f"  - {condition.replace('_', ' ').title()}")

# Save to JSON files
print("\n" + "="*80)
print("SAVING JSON FILES")
print("="*80)

with open("icd_mapping.json", "w", encoding='utf-8') as f:
    json.dump(icd_mapping, f, indent=2, ensure_ascii=False)
print("\nSaved: icd_mapping.json")

with open("critical_condition.json", "w", encoding='utf-8') as f:
    json.dump(critical_conditions, f, indent=2, ensure_ascii=False)
print("Saved: critical_condition.json")

# Generate summary report
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)
print("\nDataset: AGBonnet/augmented-clinical-notes")
print(f"Records analyzed: {len(dataset)}")
print(f"Total conditions mapped: {len(icd_mapping)}")
print(f"Critical conditions: {len(critical_conditions)}")
print("\nConditions by severity:")
severity_counts = Counter([data['severity'] for data in icd_mapping.values()])
for severity, count in severity_counts.most_common():
    print(f"  {severity.title()}: {count}")

print("\n" + "="*80)
print("COMPLETE")
print("="*80)
print("\nGenerated files:")
print(f"  - icd_mapping.json ({len(icd_mapping)} conditions with ICD-10 codes)")
print(f"  - critical_condition.json ({len(critical_conditions)} critical conditions)")
print("\nThese files are ready for use in medical NLP applications!")
