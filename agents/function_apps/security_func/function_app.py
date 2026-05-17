import azure.functions as func

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.security.agent import SecurityAgent
from agentic_ai.security.sentinel_connector import SentinelConnector

app = func.FunctionApp()


@app.timer_trigger(schedule="0 */15 * * * *", arg_name="timer", run_on_startup=False)
async def security_scan(timer: func.TimerRequest) -> None:
    config = AgentConfig.from_env()
    logger = get_logger("security")
    credential = get_credential()

    kernel = create_kernel(config)
    governance = GovernanceGate(config, logger)
    sentinel = SentinelConnector(credential, config.log_analytics_workspace_id)

    agent = SecurityAgent(kernel, governance, sentinel, logger)
    await agent.assess_incidents()


@app.route(route="assess", methods=["POST"])
async def security_on_demand(req: func.HttpRequest) -> func.HttpResponse:
    config = AgentConfig.from_env()
    logger = get_logger("security")
    credential = get_credential()

    kernel = create_kernel(config)
    governance = GovernanceGate(config, logger)
    sentinel = SentinelConnector(credential, config.log_analytics_workspace_id)

    agent = SecurityAgent(kernel, governance, sentinel, logger)
    results = await agent.assess_incidents()

    import json
    return func.HttpResponse(
        body=json.dumps(results),
        mimetype="application/json",
    )
