# Power BI Executive Reports

## Setup

1. Open Power BI Desktop
2. Get Data > Azure > Azure Log Analytics
3. Enter workspace ID from Phase 1 outputs: `terraform output log_analytics_workspace_guid`
4. Authenticate with your Azure AD credentials
5. Import the KQL queries from `../kql_queries/` as data sources

## Recommended Reports

| Report | Data Source | Refresh |
|--------|------------|---------|
| Agent ROI Summary | agent_activity.kql + cost_trends.kql | Daily |
| Incident Response | incident_mttr.kql | Hourly |
| Compliance Status | policy_compliance.kql | Daily |
| Capacity Overview | capacity_forecast.kql | Every 4 hours |

## Fabric Migration (Phase 4)

In Phase 4, migrate from Power BI direct queries to Microsoft Fabric:
1. Create a Fabric workspace linked to the Azure subscription
2. Set up a Lakehouse to ingest Log Analytics data
3. Build Fabric notebooks for advanced analytics
4. Connect Power BI reports to the Fabric Lakehouse
