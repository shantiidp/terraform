from typing import Annotated

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import PolicyClient
from semantic_kernel.functions import kernel_function


class PolicyCheckPlugin:
    def __init__(self, credential: DefaultAzureCredential, subscription_id: str) -> None:
        self.client = PolicyClient(credential, subscription_id)
        self.subscription_id = subscription_id

    @kernel_function(
        name="check_compliance",
        description="Check Azure Policy compliance state for a scope",
    )
    async def check_compliance(
        self,
        scope: Annotated[str, "Scope to check (subscription or resource group ID)"] = "",
    ) -> str:
        if not scope:
            scope = f"/subscriptions/{self.subscription_id}"

        states = self.client.policy_states.list_query_results_for_subscription(
            policy_states_resource="latest",
            subscription_id=self.subscription_id,
        )

        compliant = 0
        non_compliant = 0
        details = []

        for state in states:
            if state.compliance_state == "Compliant":
                compliant += 1
            else:
                non_compliant += 1
                if len(details) < 20:
                    details.append(
                        f"- {state.resource_id}: {state.policy_definition_name} ({state.compliance_state})"
                    )

        summary = f"Compliance: {compliant} compliant, {non_compliant} non-compliant\n"
        if details:
            summary += "Non-compliant resources:\n" + "\n".join(details)

        return summary

    @kernel_function(
        name="list_policy_assignments",
        description="List active policy assignments",
    )
    async def list_policy_assignments(self) -> str:
        assignments = self.client.policy_assignments.list()
        lines = [
            f"- {a.display_name or a.name}: {a.policy_definition_id}"
            for a in assignments
        ]
        return f"Policy assignments ({len(lines)}):\n" + "\n".join(lines) if lines else "No policy assignments found."
