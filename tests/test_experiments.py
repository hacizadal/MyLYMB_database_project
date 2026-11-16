"""Static experiment contract tests (no database required)."""
import pytest
from experiments import CHANGES, ALGORITHMS, build_alter_sql


def test_online_copy_is_requested_explicitly():
    assert ALGORITHMS["copy"][0] == "ALGORITHM=COPY, LOCK=NONE"
    assert "expected to refuse" not in ALGORITHMS["copy"][1]


def test_index_instant_is_a_negative_test_candidate():
    sql = build_alter_sql("add-index", "instant")
    assert "ADD INDEX" in sql and "ALGORITHM=INSTANT" in sql


@pytest.mark.parametrize("change", CHANGES)
@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_all_matrix_sql_statements_have_algorithm(change, algorithm):
    sql = build_alter_sql(change, algorithm)
    assert sql.startswith("ALTER TABLE ")
    assert ("ALGORITHM=" in sql) == (algorithm != "default")
