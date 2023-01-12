from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter
)

metric_exporter = OTLPMetricExporter()

metric_reader = PeriodicExportingMetricReader(
    exporter=[metric_exporter],
    export_interval_millis=3_000,
)

meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# CPU Meter
cpu_meter = metrics.get_meter_provider().get_meter("cpu-meter")

def cpu_gauge_func(options):
    # This function gets called every time OpenTelemetry takes a reading
    # It yields a value in the Observation
    # CPU measurement should take place within here

    val = 34

    yield metrics.Observation(val)

cpu_gauge = cpu_meter.create_observable_gauge(
    "cpu_gauge",

)