from datetime import timedelta
from typing import Annotated

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from semantic_kernel.functions import kernel_function


class MonitorQueryPlugin:
    def __init__(self, credential: DefaultAzureCredential, workspace_id: str) -> None:
        self.client = LogsQueryClient(credential)
        self.workspace_id = workspace_id

    @kernel_function(
        name="run_kql_query",
        description="Execute a KQL query against Azure Log Analytics",
    )
    async def run_kql_query(
        self,
        query: Annotated[str, "KQL query string"],
        timespan_hours: Annotated[int, "Timespan in hours to query"] = 24,
    ) -> str:
        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=timedelta(hours=timespan_hours),
        )

        if response.status == LogsQueryStatus.SUCCESS:
            rows = []
            for table in response.tables:
                columns = [col.name for col in table.columns]
                rows.append(" | ".join(columns))
                for row in table.rows[:50]:
                    rows.append(" | ".join(str(v) for v in row))
            return "\n".join(rows) if rows else "Query returned no results."

        return f"Query failed: {response.partial_error}"

    @kernel_function(
        name="get_recent_alerts",
        description="Get recent Azure Monitor alerts",
    )
    async def get_recent_alerts(
        self,
        severity: Annotated[str, "Alert severity filter (Sev0, Sev1, Sev2, Sev3, Sev4)"] = "",
        timespan_hours: Annotated[int, "Hours to look back"] = 4,
    ) -> str:
        query = "AlertsManagementResources | where type == 'microsoft.alertsmanagement/alerts'"
        if severity:
            query += f" | where properties.essentials.severity == '{severity}'"
        query += " | project name, properties.essentials.severity, properties.essentials.monitorCondition, properties.essentials.startDateTime"
        query += " | order by properties_essentials_startDateTime desc | take 20"

        return await self.run_kql_query(query, timespan_hours)
