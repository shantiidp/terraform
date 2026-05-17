import azure.functions as func

from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.deployment.agent import DeploymentAgent

app = func.FunctionApp()


@app.route(route="deploy", methods=["POST"])
async def plan_deployment(req: func.HttpRequest) -> func.HttpResponse:
    config = AgentConfig.from_env()
    logger = get_logger("deployment")

    kernel = create_kernel(config)
    governance = GovernanceGate(config, logger)

    agent = DeploymentAgent(kernel, governance, logger)

    body = req.get_json()
    plan = await agent.plan_deployment(
        pipeline_info=body.get("pipeline_info", ""),
        target_env=body.get("target_env", "dev"),
        changes=body.get("changes", ""),
    )

    return func.HttpResponse(
        body=plan.model_dump_json(),
        mimetype="application/json",
    )
