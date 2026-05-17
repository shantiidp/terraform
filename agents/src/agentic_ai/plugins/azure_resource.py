from typing import Annotated

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from semantic_kernel.functions import kernel_function


class AzureResourcePlugin:
    def __init__(self, credential: DefaultAzureCredential, subscription_id: str) -> None:
        self.client = ResourceManagementClient(credential, subscription_id)
        self.subscription_id = subscription_id

    @kernel_function(
        name="list_resources",
        description="List Azure resources in a resource group with optional type filter",
    )
    async def list_resources(
        self,
        resource_group: Annotated[str, "Name of the resource group"],
        resource_type: Annotated[str, "Filter by resource type (e.g., Microsoft.Compute/virtualMachines)"] = "",
    ) -> str:
        filter_str = f"resourceType eq '{resource_type}'" if resource_type else None
        resources = self.client.resources.list_by_resource_group(
            resource_group, filter=filter_str
        )

        lines = []
        for r in resources:
            lines.append(f"- {r.name} ({r.type}) [{r.location}] tags={r.tags or {}}")

        return f"Resources in {resource_group} ({len(lines)} found):\n" + "\n".join(lines) if lines else "No resources found."

    @kernel_function(
        name="get_resource_details",
        description="Get detailed information about a specific Azure resource",
    )
    async def get_resource_details(
        self,
        resource_id: Annotated[str, "Full Azure resource ID"],
    ) -> str:
        resource = self.client.resources.get_by_id(resource_id, api_version="2023-07-01")
        return (
            f"Name: {resource.name}\n"
            f"Type: {resource.type}\n"
            f"Location: {resource.location}\n"
            f"SKU: {resource.sku}\n"
            f"Tags: {resource.tags}\n"
            f"Properties: {resource.properties}"
        )

    @kernel_function(
        name="list_resource_groups",
        description="List all resource groups in the subscription",
    )
    async def list_resource_groups(self) -> str:
        groups = self.client.resource_groups.list()
        lines = [f"- {g.name} [{g.location}] tags={g.tags or {}}" for g in groups]
        return f"Resource groups ({len(lines)}):\n" + "\n".join(lines)
