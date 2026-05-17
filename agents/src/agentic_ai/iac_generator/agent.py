import logging
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, RiskLevel
from agentic_ai.iac_generator.validator import validate_terraform


PROMPTS_DIR = Path(__file__).parent / "prompts"


class IaCGeneratorAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger) -> None:
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def generate(self, request: str, location: str = "eastus2", environment: str = "dev") -> dict:
        self.logger.info("Generating Terraform for: %s", request[:100])

        prompt = (PROMPTS_DIR / "generate_tf.txt").read_text()

        response = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                request=request,
                location=location,
                environment=environment,
            ),
            template_format="semantic-kernel",
        )

        hcl_content = str(response)

        validation = validate_terraform(hcl_content)
        self.logger.info(
            "Validation: valid=%s errors=%d warnings=%d",
            validation.valid,
            len(validation.errors),
            len(validation.warnings),
        )

        action = AgentAction(
            agent_name="iac_generator",
            action_type="generate_terraform",
            description=f"Generate Terraform: {request[:100]}",
            risk_level=RiskLevel.LOW,
        )
        await self.governance.request_approval(action)

        return {
            "hcl": hcl_content,
            "valid": validation.valid,
            "errors": validation.errors,
            "warnings": validation.warnings,
        }
