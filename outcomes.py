
"""Classify successful ALTERs, expected refusals and unexpected failures."""

EXPECTED_1846 = {
    ("change-type", "inplace"),
    ("change-type", "nocopy"),
    ("change-type", "instant"),
    ("add-index", "instant"),
    ("add-fk", "inplace"),
    ("add-fk", "nocopy"),
    ("add-fk", "instant"),
    ("add-fk-fkchecks-off", "instant"),
    ("widen-column-rebuild", "instant"),
    ("widen-column-rebuild", "nocopy"),
    ("widen-column-rebuild", "inplace"),
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
