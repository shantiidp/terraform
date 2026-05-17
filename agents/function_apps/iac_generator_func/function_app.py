import azure.functions as func

from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.iac_generator.agent import IaCGeneratorAgent

app = func.FunctionApp()


@app.route(route="generate", methods=["POST"])
async def generate_iac(req: func.HttpRequest) -> func.HttpResponse:
    config = AgentConfig.from_env()
    logger = get_logger("iac_generator")

    kernel = create_kernel(config)
    governance = GovernanceGate(config, logger)

    agent = IaCGeneratorAgent(kernel, governance, logger)

    body = req.get_json()
    result = await agent.generate(
        request=body["request"],
        location=body.get("location", "eastus2"),
        environment=body.get("environment", "dev"),
    )

    import json
    return func.HttpResponse(
        body=json.dumps(result),
        mimetype="application/json",
    )
