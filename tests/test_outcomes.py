import pandas as pd
import pytest
from outcomes import classify_outcome
from analyze_results import alter_summary

@pytest.mark.parametrize("change,algorithm", [
    ("change-type", "inplace"), ("change-type", "nocopy"),
    ("change-type", "instant"), ("add-index", "instant"),
    ("add-fk", "inplace"), ("add-fk", "nocopy"),
    ("add-fk", "instant"), ("add-fk-fkchecks-off", "instant"),
])
def test_expected_rejections(change, algorithm):
    assert classify_outcome(change, algorithm, "failure", 1846) == "expected_rejection"

def test_other_errors_are_not_suppressed():
    assert classify_outcome("add-index", "instant", "failure", 1205) == "unexpected_failure"
    assert classify_outcome("add-index", "copy", "failure", 1846) == "unexpected_failure"
    assert classify_outcome("add-index", "instant", "success", "") == "success"

def test_summary_counts_outcomes_and_variance():
    frame = pd.DataFrame([
        dict(change="add-index", requested_algorithm="instant", status="failure", errno=1846, error="not supported", duration_seconds=.03),
        dict(change="add-index", requested_algorithm="instant", status="failure", errno=1205, error="timeout", duration_seconds=.04),
        dict(change="add-index", requested_algorithm="copy", status="success", errno="", error="", duration_seconds=.10),
        dict(change="add-index", requested_algorithm="copy", status="success", errno="", error="", duration_seconds=.20),
    ])
    s = alter_summary(frame)
    instant = s[s.algorithm == "instant"].iloc[0]
    assert instant.expected_rejections == 1 and instant.unexpected_failures == 1
    copy = s[s.algorithm == "copy"].iloc[0]
    assert copy.median_s == pytest.approx(.15)
    assert copy.stddev_s > 0
