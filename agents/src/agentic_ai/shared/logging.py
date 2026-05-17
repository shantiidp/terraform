import logging
import uuid

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_initialized = False


def _init_telemetry(connection_string: str | None = None) -> None:
    global _initialized
    if _initialized:
        return

    provider = TracerProvider()

    if connection_string:
        from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

        exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)
    _initialized = True


def get_logger(agent_name: str, connection_string: str | None = None) -> logging.Logger:
    _init_telemetry(connection_string)

    logger = logging.getLogger(f"agentic_ai.{agent_name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f"%(asctime)s [%(levelname)s] [{agent_name}] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def new_correlation_id() -> str:
    return str(uuid.uuid4())
