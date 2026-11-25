# Verification and remaining work

- Team-run MariaDB 11.4.13 benchmark: 245 ALTERs, 190 successes, 55 expected refusals; all 245 workload CSVs included.
- Advanced probes: 30 measured outcomes included. README updated from raw results.
- Four workload errors occurred in one blocking foreign-key run; no unexpected ALTER failures.
- Replication remains a protocol, not a measured experiment. RAM, storage type and Docker resource limits remain unrecorded. CI and clean-checkout integration have not been independently verified in this editing environment.
- Review and commit to main; follow course AI-use rules. No remote changes made.
