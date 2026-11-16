"""Interpret deliberately incompatible DDL requests separately from infrastructure errors.

The raw status in alter_results.csv remains unchanged; this module adds a
research-level classification. Only errno 1846 in known incompatible
combinations is expected. Any other error must remain visible.
"""

EXPECTED_1846 = {
    ("change-type", "inplace"), ("change-type", "nocopy"),
    ("change-type", "instant"), ("add-index", "instant"),
    ("add-fk", "inplace"), ("add-fk", "nocopy"),
    ("add-fk", "instant"), ("add-fk-fkchecks-off", "instant"),
}


def classify_outcome(change, algorithm, status, errno):
    if status == "success":
        return "success"
    try:
        number = int(errno)
    except (ValueError, TypeError):
        number = None
    if number == 1846 and (change, algorithm) in EXPECTED_1846:
        return "expected_rejection"
    return "unexpected_failure"
