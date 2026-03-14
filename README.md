# Clinical AI Reliability Evaluation Framework

## Overview

This project implements an evaluation framework for analyzing the reliability of a clinical AI pipeline that extracts structured medical entities from OCR-processed clinical records.

Healthcare AI systems often process large volumes of medical charts using OCR and NLP pipelines. While these systems can extract many clinical entities, errors in reasoning such as incorrect entity classification, temporality interpretation, or subject attribution can lead to incorrect clinical insights.

This framework evaluates the reliability of such AI pipelines by analyzing their extracted entities and computing error metrics across several clinical reasoning dimensions.

The goal of this project is **not to retrain the model**, but to **analyze its outputs and identify reliability weaknesses**.

---

## System Pipeline

The evaluated pipeline consists of the following stages:

1. **OCR Pipeline**

   Converts scanned medical charts into structured markdown text.

2. **Clinical Entity Extraction**

   A clinical NLP system extracts structured medical entities from the OCR output.

3. **Evaluation Framework (this project)**

   Analyzes extracted entities and computes reliability metrics.

---

## Evaluation Metrics

The following reliability metrics are computed for each chart.

### Entity Type Error Rate

Measures incorrect classification of medical entities.

Example error:

Entity: deceased
Type: PROCEDURE


---

### Assertion Error Rate

Measures errors in polarity interpretation.

Example:
Text: Are you a smoker? No
Extracted entity: current smoker
Assertion: POSITIVE


---

### Temporality Error Rate

Evaluates whether conditions are correctly classified as:

- CURRENT
- CLINICAL_HISTORY
- UPCOMING

Example:
Text: history of hypertension
Temporality: CURRENT (incorrect)


---

### Subject Attribution Error Rate

Detects whether medical conditions are attributed to the correct subject.

Example:
Text: Father had hypertension
Subject labeled as PATIENT


Correct subject should be **FAMILY_MEMBER**.

---

### Event Date Accuracy

Measures how accurately event dates are extracted from the clinical text.

---

### Attribute Completeness

Measures whether entities contain all required metadata fields.

Required attributes include:

- entity_type
- assertion
- temporality
- subject

---

### Duplicate Entity Rate

Measures redundant entity extraction within the same clinical chart.

Duplicate extractions may indicate issues in the extraction pipeline.

---

### Reliability Score

An aggregated reliability score summarizing overall system performance.

---

## Repository Structure


clinical-ai-evaluation
│
├── output/
│ ├── chart_1.json
│ ├── chart_2.json
│ └── ...
│
├── test.py
├── run_all.py
├── rules.py
│
├── report.md
└── README.md



---

## Running the Evaluation

The evaluation script processes each chart and generates an evaluation report.

Run:
python3 run_all.py


This will process all files inside:


test_data/


and generate evaluation reports inside:


output/


---

## Example Output

Each clinical chart produces a JSON evaluation report.

Example:

```json
{
  "file_name": "019M72177_N991-796129_20241213.json",

  "entity_type_error_rate": {
    "MEDICINE": 0.0,
    "PROBLEM": 0.03,
    "PROCEDURE": 0.0,
    "TEST": 0.01,
    "VITAL_NAME": 0.0,
    "IMMUNIZATION": 0.0,
    "MEDICAL_DEVICE": 0.0,
    "MENTAL_STATUS": 0.0,
    "SDOH": 0.0,
    "SOCIAL_HISTORY": 0.02
  },

  "assertion_error_rate": {
    "POSITIVE": 0.65,
    "NEGATIVE": 0.02,
    "UNCERTAIN": 0.01
  },

  "temporality_error_rate": {
    "CURRENT": 0.24,
    "CLINICAL_HISTORY": 0.03,
    "UPCOMING": 0.01,
    "UNCERTAIN": 0.0
  },

  "subject_error_rate": {
    "PATIENT": 0.14,
    "FAMILY_MEMBER": 0.01
  },

  "event_date_accuracy": 0.78,
  "attribute_completeness": 1.0,
  "duplicate_entity_rate": 0.04,
  "reliability_score": 0.73
}
Dataset Summary

Dataset contains 30 clinical charts.

Typical observed results:

Metric	Typical Range
Entity Type Error	0–5%
Assertion Error	40–65%
Temporality Error	15–30%
Subject Error	10–20%
Attribute Completeness	~100%
Reliability Score	~0.70
