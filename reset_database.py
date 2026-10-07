"""Reset only the schemalab tables, then generate and verify the baseline."""
from pathlib import Path
import subprocess
from generate_data import generate_data


def reset_database():
    schema_path = Path(__file__).resolve().with_name("schema.sql")
    print("Resetting schemalab tables and loading schema.sql...", flush=True)
    # Feed SQL through stdin: works on Windows without shell redirection.
    # The password must be attached to -p: -plabpass, with no space.
    with schema_path.open("rb") as schema_file:
        subprocess.run(
            ["docker", "exec", "-i", "mariadb-lab", "mariadb",
             "-uroot", "-plabpass", "schemalab"],
            stdin=schema_file, check=True,
        )
    # Any schema/generation/count failure stops the test before ALTER runs.
    generate_data()
    print("Reset complete: verified baseline is ready.", flush=True)


if __name__ == "__main__":
    reset_database()
