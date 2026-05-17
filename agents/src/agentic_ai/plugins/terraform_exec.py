import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

from semantic_kernel.functions import kernel_function


class TerraformExecPlugin:
    @kernel_function(
        name="validate_terraform",
        description="Validate generated Terraform HCL syntax",
    )
    async def validate_terraform(
        self,
        hcl_content: Annotated[str, "Terraform HCL content to validate"],
    ) -> str:
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
                return f"Init failed:\n{init_result.stderr}"

            validate_result = subprocess.run(
                ["terraform", "validate", "-json"],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            return validate_result.stdout

    @kernel_function(
        name="format_terraform",
        description="Format Terraform HCL content",
    )
    async def format_terraform(
        self,
        hcl_content: Annotated[str, "Terraform HCL content to format"],
    ) -> str:
        result = subprocess.run(
            ["terraform", "fmt", "-"],
            input=hcl_content,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return f"Format failed:\n{result.stderr}"

        return result.stdout
