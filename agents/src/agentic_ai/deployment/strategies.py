from dataclasses import dataclass
from enum import Enum


class DeploymentStrategy(str, Enum):
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    DIRECT = "direct"


@dataclass
class StrategyConfig:
    name: DeploymentStrategy
    description: str
    health_check_wait_seconds: int
    canary_percentage: int
    requires_approval: bool


STRATEGY_CONFIGS: dict[DeploymentStrategy, StrategyConfig] = {
    DeploymentStrategy.BLUE_GREEN: StrategyConfig(
        name=DeploymentStrategy.BLUE_GREEN,
        description="Deploy to inactive slot, swap after health check",
        health_check_wait_seconds=300,
        canary_percentage=0,
        requires_approval=True,
    ),
    DeploymentStrategy.CANARY: StrategyConfig(
        name=DeploymentStrategy.CANARY,
        description="Route small percentage of traffic to new version",
        health_check_wait_seconds=600,
        canary_percentage=10,
        requires_approval=True,
    ),
    DeploymentStrategy.ROLLING: StrategyConfig(
        name=DeploymentStrategy.ROLLING,
        description="Gradually replace instances with new version",
        health_check_wait_seconds=120,
        canary_percentage=0,
        requires_approval=False,
    ),
    DeploymentStrategy.DIRECT: StrategyConfig(
        name=DeploymentStrategy.DIRECT,
        description="Direct deployment, suitable for non-production",
        health_check_wait_seconds=30,
        canary_percentage=0,
        requires_approval=False,
    ),
}


def get_strategy(name: DeploymentStrategy) -> StrategyConfig:
    return STRATEGY_CONFIGS[name]
