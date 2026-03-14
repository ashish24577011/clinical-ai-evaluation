import json
import sys
from rules import *

def evaluate(entities):

    total = len(entities)

    entity_errors = 0
    assertion_errors = 0
    temporality_errors = 0
    subject_errors = 0
    completeness_errors = 0

    for e in entities:

        text = e.get("text","").lower()
        assertion = e.get("assertion")
        temporality = e.get("temporality")
        subject = e.get("subject")
        entity_type = e.get("entity_type")

        # Assertion error detection
        for neg in NEGATIONS:
            if neg in text and assertion == "POSITIVE":
                assertion_errors += 1

        # Temporality error detection
        for h in HISTORY_WORDS:
            if h in text and temporality == "CURRENT":
                temporality_errors += 1

        # Subject attribution errors
        for f in FAMILY_WORDS:
            if f in text and subject == "PATIENT":
                subject_errors += 1

        # Example entity type error rule
        if "deceased" in text and entity_type == "PROCEDURE":
            entity_errors += 1

        # Attribute completeness check
        if None in [assertion, temporality, subject, entity_type]:
            completeness_errors += 1

    # Overall reliability score
    reliability_score = 1 - (
        entity_errors +
        assertion_errors +
        temporality_errors +
        subject_errors
    ) / (4 * total)

    return {
        "entity_type_error_rate": entity_errors/total,
        "assertion_error_rate": assertion_errors/total,
        "temporality_error_rate": temporality_errors/total,
        "subject_error_rate": subject_errors/total,
        "attribute_completeness": 1 - completeness_errors/total,
        "reliability_score": reliability_score
    }


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file) as f:
        data = json.load(f)

    results = evaluate(data)

    output = {
        "file_name": input_file.split("/")[-1],
        **results
    }

    with open(output_file,"w") as f:
        json.dump(output,f,indent=2)


if __name__ == "__main__":
    main()
