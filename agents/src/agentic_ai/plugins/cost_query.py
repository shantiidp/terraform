from typing import Annotated

from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from semantic_kernel.functions import kernel_function


class CostQueryPlugin:
    def __init__(self, credential: DefaultAzureCredential) -> None:
        self.client = CostManagementClient(credential)

    @kernel_function(
        name="query_costs",
        description="Query Azure cost data for a subscription over a time period",
    )
    async def query_costs(
        self,
        scope: Annotated[str, "Azure scope (e.g., /subscriptions/{id})"],
        timeframe: Annotated[str, "Timeframe: MonthToDate, BillingMonthToDate, TheLastMonth, TheLastBillingMonth, WeekToDate, Custom"] = "MonthToDate",
    ) -> str:
        query = {
            "type": "ActualCost",
            "timeframe": timeframe,
            "dataset": {
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {"name": "Cost", "function": "Sum"},
                    "totalCostUSD": {"name": "CostUSD", "function": "Sum"},
                },
                "grouping": [
                    {"type": "Dimension", "name": "ServiceName"},
                    {"type": "Dimension", "name": "ResourceGroup"},
                ],
            },
        }

        result = self.client.query.usage(scope=scope, parameters=query)

        rows = []
        if result.rows:
            for row in result.rows[:50]:
                rows.append(str(row))

        return f"Cost data ({len(rows)} rows):\n" + "\n".join(rows)

    @kernel_function(
        name="get_cost_by_resource",
        description="Get cost breakdown by individual resource",
    )
    async def get_cost_by_resource(
        self,
        scope: Annotated[str, "Azure scope"],
    ) -> str:
        query = {
            "type": "ActualCost",
            "timeframe": "MonthToDate",
            "dataset": {
                "granularity": "None",
                "aggregation": {
                    "totalCost": {"name": "Cost", "function": "Sum"},
                },
                "grouping": [
                    {"type": "Dimension", "name": "ResourceId"},
                    {"type": "Dimension", "name": "ResourceType"},
                ],
                "sorting": [{"direction": "descending", "name": "Cost"}],
            },
        }

        result = self.client.query.usage(scope=scope, parameters=query)

        rows = []
        if result.rows:
            for row in result.rows[:20]:
                rows.append(str(row))

        return f"Top resources by cost:\n" + "\n".join(rows)
