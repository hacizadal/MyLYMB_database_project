import pandas as pd
import pytest

from analyze_results import fig_p95


def phases(*names):
    return pd.DataFrame([
        dict(change='widen-column-60', algorithm='instant', run_id='r1',
             phase=name, alter_status='success', p95_ms=1.5)
        for name in names
    ])


@pytest.mark.parametrize('phase', ['baseline', 'during', 'after'])
def test_missing_workload_phase(tmp_path, phase):
    output = tmp_path / 'p95.png'
    assert fig_p95(phases(phase), output) is False
    assert not output.exists()


def test_empty_workload(tmp_path):
    assert fig_p95(pd.DataFrame(), tmp_path / 'p95.png') is False


def test_complete_workload(tmp_path):
    output = tmp_path / 'p95.png'
    assert fig_p95(phases('baseline', 'during'), output) is True
    assert output.stat().st_size > 0


def test_phases_from_different_runs_not_paired(tmp_path):
    df = phases('baseline', 'during')
    df.loc[1, 'run_id'] = 'r2'
    assert fig_p95(df, tmp_path / 'p95.png') is False


def test_refused_alter_not_plotted(tmp_path):
    df = phases('baseline', 'during')
    df['alter_status'] = 'failure'
    assert fig_p95(df, tmp_path / 'p95.png') is False
