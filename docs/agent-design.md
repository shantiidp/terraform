# Agent Design Patterns

## Agent Structure

Every agent follows this pattern:

```
agents/src/agentic_ai/{agent_name}/
├── __init__.py
├── agent.py          # Main agent class
├── prompts/
│   ├── system.txt    # Agent persona and rules
│   └── {task}.txt    # Task-specific prompt templates
└── {helpers}.py      # Agent-specific logic (optional)
```

## Agent Lifecycle

```python
# 1. Configuration
config = AgentConfig.from_env()
logger = get_logger("agent_name")

# 2. Plugin setup
plugins = [CostQueryPlugin(credential), MonitorQueryPlugin(...)]

# 3. Kernel creation
kernel = create_kernel(config, plugins)

# 4. Governance gate
governance = GovernanceGate(config, logger)

# 5. Agent instantiation
agent = MyAgent(kernel, governance, logger)

# 6. Execution
result = await agent.do_work(...)
```

## Governance Contract

Every mutating action MUST go through `GovernanceGate.request_approval()`:

| Risk Level | Behavior |
|-----------|----------|
| LOW | Auto-approved, logged |
| MEDIUM | Routed to approval workflow |
| HIGH | Routed to approval workflow, requires senior approver |
| CRITICAL | Always requires human approval, alerts security team |

## Semantic Kernel Plugins

Plugins provide the "tools" that agents can use. Each plugin is a class with `@kernel_function` decorated methods:

- **CostQueryPlugin**: Azure Cost Management API
- **MonitorQueryPlugin**: KQL queries against Log Analytics
- **AzureResourcePlugin**: ARM resource operations
- **PolicyCheckPlugin**: Azure Policy compliance state
- **TerraformExecPlugin**: Terraform validation and formatting

## Prompt Engineering

- System prompts define the agent's role, capabilities, and safety rules
- Task prompts use `{{$variable}}` syntax for Semantic Kernel template variables
- All prompts are stored as `.txt` files (not hardcoded in Python)
- Prompts should be treated as versioned artifacts

## Adding a New Agent

1. Create directory under `agents/src/agentic_ai/{name}/`
2. Write system prompt defining the agent's role
3. Implement `agent.py` following the standard pattern
4. Create Function App entry point in `agents/function_apps/{name}_func/`
5. Add Terraform module call in the appropriate phase
6. Add RBAC role assignments for the agent's managed identity
7. Add tests in `agents/tests/test_{name}/`
