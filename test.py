import json
import sys
from collections import defaultdict

ENTITY_TYPES = [
    "MEDICINE","PROBLEM","PROCEDURE","TEST","VITAL_NAME",
    "IMMUNIZATION","MEDICAL_DEVICE","MENTAL_STATUS","SDOH","SOCIAL_HISTORY"
]

ASSERTIONS = ["POSITIVE","NEGATIVE","UNCERTAIN"]
TEMPORALITY = ["CURRENT","CLINICAL_HISTORY","UPCOMING","UNCERTAIN"]
SUBJECTS = ["PATIENT","FAMILY_MEMBER"]


def evaluate(data):

    entity_counts = defaultdict(int)
    entity_errors = defaultdict(int)

    assertion_counts = defaultdict(int)
    assertion_errors = defaultdict(int)

    temporality_counts = defaultdict(int)
    temporality_errors = defaultdict(int)

    subject_counts = defaultdict(int)
    subject_errors = defaultdict(int)

    total_entities = len(data)

    missing_attr = 0
    event_date_correct = 0
    event_date_total = 0

    for e in data:

        etype = e.get("entity_type")
        assertion = e.get("assertion")
        temporality = e.get("temporality")
        subject = e.get("subject")

        if etype in ENTITY_TYPES:
            entity_counts[etype] += 1
        else:
            entity_errors[etype] += 1

        if assertion in ASSERTIONS:
            assertion_counts[assertion] += 1
        else:
            assertion_errors[assertion] += 1

        if temporality in TEMPORALITY:
            temporality_counts[temporality] += 1
        else:
            temporality_errors[temporality] += 1

        if subject in SUBJECTS:
            subject_counts[subject] += 1
        else:
            subject_errors[subject] += 1

        if "event_date" in e:
            event_date_total += 1
            if e["event_date"]:
                event_date_correct += 1

        if None in [etype, assertion, temporality, subject]:
            missing_attr += 1

    entity_rate = {k: entity_errors[k]/entity_counts[k] if entity_counts[k] else 0 for k in ENTITY_TYPES}
    assertion_rate = {k: assertion_errors[k]/assertion_counts[k] if assertion_counts[k] else 0 for k in ASSERTIONS}
    temporality_rate = {k: temporality_errors[k]/temporality_counts[k] if temporality_counts[k] else 0 for k in TEMPORALITY}
    subject_rate = {k: subject_errors[k]/subject_counts[k] if subject_counts[k] else 0 for k in SUBJECTS}

    event_date_accuracy = event_date_correct/event_date_total if event_date_total else 0
    attribute_completeness = 1 - (missing_attr/total_entities if total_entities else 0)

    return entity_rate, assertion_rate, temporality_rate, subject_rate, event_date_accuracy, attribute_completeness


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as f:
        data = json.load(f)

    entity_rate, assertion_rate, temporality_rate, subject_rate, event_date_accuracy, attribute_completeness = evaluate(data)

    output = {
        "file_name": input_file.split("/")[-1],
        "entity_type_error_rate": entity_rate,
        "assertion_error_rate": assertion_rate,
        "temporality_error_rate": temporality_rate,
        "subject_error_rate": subject_rate,
        "event_date_accuracy": event_date_accuracy,
        "attribute_completeness": attribute_completeness
    }

    with open(output_file,"w") as f:
        json.dump(output,f,indent=2)


if __name__ == "__main__":
    main()
