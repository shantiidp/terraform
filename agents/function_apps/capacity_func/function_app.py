import azure.functions as func

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.kernel_factory import create_kernel
from agentic_ai.shared.logging import get_logger
from agentic_ai.plugins.monitor_query import MonitorQueryPlugin
from agentic_ai.capacity_planner.agent import CapacityPlannerAgent

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 */4 * * *", arg_name="timer", run_on_startup=False)
async def capacity_check(timer: func.TimerRequest) -> None:
    config = AgentConfig.from_env()
    logger = get_logger("capacity_planner")
    credential = get_credential()

    plugins = [MonitorQueryPlugin(credential, config.log_analytics_workspace_id)]
    kernel = create_kernel(config, plugins)
    governance = GovernanceGate(config, logger)

    agent = CapacityPlannerAgent(kernel, governance, logger)

    for resource_type in ["Processor", "Memory", "LogicalDisk"]:
        await agent.forecast(resource_type, forecast_hours=24)
