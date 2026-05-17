from dataclasses import dataclass


@dataclass
class MetricPoint:
    timestamp: str
    value: float


@dataclass
class ForecastResult:
    predicted_value: float
    confidence: float
    trend: str  # "increasing", "stable", "decreasing"
    hours_to_threshold: float | None


def simple_linear_forecast(
    data_points: list[MetricPoint],
    forecast_hours: int = 24,
    threshold: float = 80.0,
) -> ForecastResult:
    if len(data_points) < 2:
        return ForecastResult(
            predicted_value=data_points[0].value if data_points else 0,
            confidence=0.1,
            trend="stable",
            hours_to_threshold=None,
        )

    n = len(data_points)
    x_vals = list(range(n))
    y_vals = [p.value for p in data_points]

    x_mean = sum(x_vals) / n
    y_mean = sum(y_vals) / n

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)

    if denominator == 0:
        return ForecastResult(predicted_value=y_mean, confidence=0.5, trend="stable", hours_to_threshold=None)

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    predicted = slope * (n + forecast_hours) + intercept

    if abs(slope) < 0.01:
        trend = "stable"
    elif slope > 0:
        trend = "increasing"
    else:
        trend = "decreasing"

    hours_to_threshold = None
    if slope > 0 and y_vals[-1] < threshold:
        hours_to_threshold = (threshold - y_vals[-1]) / slope

    confidence = min(0.9, 0.5 + (n / 100))

    return ForecastResult(
        predicted_value=max(0, min(100, predicted)),
        confidence=confidence,
        trend=trend,
        hours_to_threshold=hours_to_threshold,
    )
