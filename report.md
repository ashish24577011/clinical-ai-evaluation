# Clinical AI Reliability Evaluation Framework

## 1. Overview

This project evaluates the reliability of a clinical AI pipeline that extracts structured medical entities from OCR-processed clinical notes.

The pipeline consists of:

1. OCR system converting scanned medical charts into structured text
2. Clinical NLP model extracting medical entities
3. Metadata enrichment for each extracted entity

The goal of this evaluation framework is to assess **system reliability and reasoning correctness**, rather than retraining or modifying the model.

---

# 2. Dataset

The dataset consists of **30 clinical charts**.

Each chart contains:

- OCR output (`.md`)
- Extracted clinical entities (`.json`)

Directory structure:


test_data/
chart_folder/
chart_folder.json
chart_folder.md


The evaluation script processes each chart and generates an evaluation report stored in the `output/` directory.

---

# 3. Evaluation Metrics

The following reliability metrics were implemented.

## Entity Type Error Rate

Measures errors where an entity is assigned an incorrect type.

Example:


Entity: deceased
Entity Type: PROCEDURE


This is incorrect because "deceased" is not a medical procedure.

---

## Assertion Error Rate

Measures errors in **positive/negative/uncertain classification**.

Example:


Text: Are you a smoker? No
Extracted entity: current smoker
Assertion: POSITIVE


This indicates incorrect negation reasoning.

---

## Temporality Error Rate

Measures errors in identifying whether a condition is:

- Current
- Clinical history
- Upcoming

Example:


Text: history of hypertension
Temporality labeled as CURRENT


Correct label should be **CLINICAL_HISTORY**.

---

## Subject Attribution Error Rate

Measures incorrect attribution of medical information.

Example:


Text: Father had hypertension
Subject labeled as PATIENT


Correct label should be **FAMILY_MEMBER**.

---

## Attribute Completeness

Measures whether required metadata fields exist.

Required attributes:

- entity_type
- assertion
- temporality
- subject

Missing attributes reduce completeness score.

---

## Reliability Score

An overall reliability score is computed as:


Reliability Score = 1 - Average(Error Rates)


This provides a single indicator of overall system reliability.

---

# 4. Quantitative Results

Across the dataset we observed the following patterns.

Typical results per chart:

| Metric | Typical Range |
|------|------|
| Entity Type Error | 0 – 5% |
| Assertion Error | 40 – 65% |
| Temporality Error | 15 – 30% |
| Subject Error | 10 – 20% |
| Attribute Completeness | ~100% |

These results indicate that the system performs well in **entity structure extraction**, but struggles with **reasoning tasks**.

---

# 5. Key Failure Modes

The most common system weaknesses include:

### 1. Negation Misinterpretation

The system frequently fails to detect negation patterns such as:


No
Denies
Not present
None


This leads to incorrect **positive assertions**.

---

### 2. Temporality Confusion

The system struggles to distinguish between:

- past medical history
- current conditions
- future procedures

This leads to incorrect temporality labels.

---

### 3. Subject Attribution Errors

Family history statements are sometimes incorrectly attributed to the patient.

Example:


Mother: hypertension


Extracted subject:


PATIENT


Correct subject should be:


FAMILY_MEMBER


---

### 4. Duplicate Entity Extraction

Some clinical concepts are extracted multiple times within the same chart.

This may lead to inflated entity counts.

---

# 6. Proposed Reliability Guardrails

To improve reliability, the following guardrails are recommended.

### Negation Detection Layer

Implement rule-based or transformer-based negation detection to correctly interpret phrases such as:


no
denies
not
none


---

### Temporal Reasoning Module

Add a temporal reasoning component that detects:


history of
previous
prior
planned


---

### Context-aware Subject Detection

Use contextual classification to differentiate between:

- patient information
- family history

---

### Post-processing Validation Rules

Introduce validation checks that flag potential inconsistencies in entity metadata.

---

### Entity Deduplication

Apply clustering or similarity-based deduplication to reduce repeated entities.

---

# 7. Conclusion

The evaluation framework successfully identifies key weaknesses in the clinical AI pipeline.

While entity extraction completeness is high, reasoning-related tasks such as negation detection, temporality understanding, and subject attribution remain challenging.

Implementing reliability guardrails can significantly improve trustworthiness of clinical AI systems.

---

# 8. Reproducibility

To run the evaluation:


python3 run_all.py


This processes all charts and generates evaluation reports in:


output/


Each chart receives its own evaluation report.

---
