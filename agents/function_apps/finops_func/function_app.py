import azure.functions as func

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.plugins.cost_query import CostQueryPlugin
from agentic_ai.finops.agent import FinOpsAgent

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
async def finops_daily_analysis(timer: func.TimerRequest) -> None:
    config = AgentConfig.from_env()
    logger = get_logger("finops")
    credential = get_credential()

    plugins = [CostQueryPlugin(credential)]
    kernel = create_kernel(config, plugins)
    governance = GovernanceGate(config, logger)

    agent = FinOpsAgent(kernel, governance, logger)

    scope = f"/subscriptions/{credential.get_token('https://management.azure.com/.default')}"
    await agent.analyze_costs(scope)


@app.route(route="analyze", methods=["POST"])
async def finops_on_demand(req: func.HttpRequest) -> func.HttpResponse:
    config = AgentConfig.from_env()
    logger = get_logger("finops")
    credential = get_credential()

    body = req.get_json()
    scope = body.get("scope", "")

    plugins = [CostQueryPlugin(credential)]
    kernel = create_kernel(config, plugins)
    governance = GovernanceGate(config, logger)

    agent = FinOpsAgent(kernel, governance, logger)
    recommendations = await agent.analyze_costs(scope)

    return func.HttpResponse(
        body=str([r.model_dump() for r in recommendations]),
        mimetype="application/json",
    )
