from dataclasses import dataclass
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


@dataclass
class SecurityIncident:
    incident_id: str
    title: str
    severity: str
    status: str
    description: str
    related_alerts: list[str]


class SentinelConnector:
    def __init__(self, credential: DefaultAzureCredential, workspace_id: str) -> None:
        self.client = LogsQueryClient(credential)
        self.workspace_id = workspace_id

    async def get_recent_incidents(self, hours: int = 24) -> list[SecurityIncident]:
        query = f"""
        SecurityIncident
        | where TimeGenerated > ago({hours}h)
        | project IncidentNumber, Title, Severity, Status, Description
        | order by TimeGenerated desc
        | take 20
        """

        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
        )

        incidents = []
        if response.tables:
            for row in response.tables[0].rows:
                incidents.append(SecurityIncident(
                    incident_id=str(row[0]),
                    title=str(row[1]),
                    severity=str(row[2]),
                    status=str(row[3]),
                    description=str(row[4]),
                    related_alerts=[],
                ))
        return incidents

    async def get_incident_details(self, incident_id: str) -> dict[str, Any]:
        query = f"""
        SecurityIncident
        | where IncidentNumber == '{incident_id}'
        | join kind=leftouter SecurityAlert on $left.RelatedAnalyticRuleIds
        | project-away *1
        """

        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
        )

        return {"incident_id": incident_id, "raw_data": str(response)}
