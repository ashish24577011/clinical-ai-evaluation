# Clinical AI Reliability Evaluation

This repository implements an evaluation framework for a clinical AI pipeline that extracts structured medical entities from OCR-processed clinical charts.

## Evaluation Metrics

The system evaluates the reliability of extracted entities using:

- Entity Type Error Rate
- Assertion Error Rate
- Temporality Error Rate
- Subject Attribution Error Rate
- Attribute Completeness
- Reliability Score

## Running the Evaluation

To generate evaluation outputs:
python3 run_all.py


This processes all charts in `test_data/` and generates evaluation reports in `output/`.

## Output

Each chart produces a JSON evaluation report containing reliability metrics.
