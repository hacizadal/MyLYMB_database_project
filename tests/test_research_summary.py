"""The environment helpers must never crash a benchmark run, even if a fact cannot be read."""
import research_summary


def test_run_text_returns_none_for_missing_command():
    assert research_summary.run_text(['this-command-does-not-exist-xyz']) is None


def test_total_ram_is_positive_or_none():
    ram = research_summary.total_ram_bytes()
    assert ram is None or ram > 0


def test_environment_has_the_expected_keys():
    facts = research_summary.environment(('11.4.13-MariaDB', 1073741824, 'utf8mb4'))
    for key in ('platform', 'logical_cpus', 'ram_gib', 'docker_server_version', 'docker_memory_gib', 'server'):
        assert key in facts
    assert facts['server'][0] == '11.4.13-MariaDB'
