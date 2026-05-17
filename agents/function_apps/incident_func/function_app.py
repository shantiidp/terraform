import azure.functions as func

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.plugins.monitor_query import MonitorQueryPlugin
from agentic_ai.incident_responder.agent import IncidentResponderAgent

app = func.FunctionApp()


@app.route(route="incident", methods=["POST"])
async def handle_alert(req: func.HttpRequest) -> func.HttpResponse:
    config = AgentConfig.from_env()
    logger = get_logger("incident_responder")
    credential = get_credential()

    plugins = [MonitorQueryPlugin(credential, config.log_analytics_workspace_id)]
    kernel = create_kernel(config, plugins)
    governance = GovernanceGate(config, logger)

    agent = IncidentResponderAgent(kernel, governance, logger)
    alert_payload = req.get_json()
    diagnosis = await agent.diagnose(alert_payload)

    return func.HttpResponse(
        body=diagnosis.model_dump_json(),
        mimetype="application/json",
    )
