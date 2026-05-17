import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


def validate_terraform(hcl_content: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if "resource" not in hcl_content and "data" not in hcl_content:
        errors.append("No resource or data blocks found")

    if 'tags' not in hcl_content:
        warnings.append("No tags block found — all resources should be tagged")

    with tempfile.TemporaryDirectory() as tmpdir:
        tf_file = Path(tmpdir) / "main.tf"
        tf_file.write_text(hcl_content)

        init_result = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if init_result.returncode != 0:
            errors.append(f"terraform init failed: {init_result.stderr[:500]}")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)

        validate_result = subprocess.run(
            ["terraform", "validate", "-json"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        try:
            result_data = json.loads(validate_result.stdout)
            if not result_data.get("valid", False):
                for diag in result_data.get("diagnostics", []):
                    severity = diag.get("severity", "error")
                    summary = diag.get("summary", "Unknown error")
                    if severity == "error":
                        errors.append(summary)
                    else:
                        warnings.append(summary)
        except json.JSONDecodeError:
            errors.append(f"Could not parse validation output: {validate_result.stdout[:200]}")

    return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)
