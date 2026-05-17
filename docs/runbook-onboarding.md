# Adding a New Agent

## Step-by-Step

### 1. Create Agent Package

```
agents/src/agentic_ai/{agent_name}/
├── __init__.py
├── agent.py
└── prompts/
    ├── system.txt
    └── {task}.txt
```

### 2. Implement Agent Class

```python
class MyAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger):
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def do_work(self, ...) -> Result:
        # 1. Gather data via plugins
        # 2. Invoke LLM with prompt
        # 3. Parse response
        # 4. Request governance approval for any actions
        # 5. Execute and return result
```

### 3. Create Function App

```
agents/function_apps/{agent}_func/
├── function_app.py
└── host.json
```

### 4. Add Terraform Resources

In the appropriate phase's `main.tf`:
```hcl
module "{agent}_function" {
  source        = "../../modules/function_app"
  function_name = "{agent}"
  # ... standard config from Phase 1 outputs
}
```

### 5. Configure RBAC

Add role assignments for the agent's managed identity in the phase's `main.tf`:
```hcl
module "rbac_{agent}" {
  source = "../../modules/rbac"
  role_assignments = {
    {agent}_reader = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Reader"
      principal_id         = module.{agent}_function.identity_principal_id
    }
  }
}
```

### 6. Add Tests

```
agents/tests/test_{agent}/
├── __init__.py
└── test_agent.py
```

### 7. Update CI/CD

Add paths to the appropriate phase workflow in `.github/workflows/`.

### 8. Update Documentation

- Add agent to `governance/rbac/role_matrix.md`
- Document agent capabilities and triggers
