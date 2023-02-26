from functools import wraps
from opentelemetry.metrics import (
    Observation,
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import (
    Counter,
    MeterProvider
)
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter, 
    PeriodicExportingMetricReader,
    AggregationTemporality
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from .aggregate import AggregateModel
# this is where all classes are going to be used and this specific module is imported

aggregate = AggregateModel(30)

def all_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        aggregate.measure()
        return func(*args, **kwargs)
    return wrapper

def ram_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        aggregate.tracers["ram"].measure()
        return func(*args, **kwargs)
    return wrapper

def setup():
    # OpenTelemetry exporter setup
    temporality_delta = {Counter: AggregationTemporality.DELTA}

    exporter = OTLPMetricExporter(
        endpoint="localhost:4318",
        preferred_temporality=temporality_delta
    )

    # Gets a reading every 30000ms (30s)
    metric_reader = PeriodicExportingMetricReader(
        exporter,
        export_interval_millis=3_000,
    )

    meter_provider = MeterProvider(metric_readers=[metric_reader])
    set_meter_provider(meter_provider)

    # CPU Meter
    cpu_meter = get_meter_provider().get_meter("cpu-meter")

    def cpu_gauge_func(options):
        print("CPU GAUGE")
        # aggregate.measure()
        # metrics = aggregate.get_metrics()
        # aggregate_data = metrics["cpu"]
        # val = aggregate_data[len(aggregate_data)][2]
        val = 2222
        yield Observation(val)

    cpu_gauge = cpu_meter.create_observable_gauge(
        "cpu_gauge",
        callbacks=[cpu_gauge_func]
    )


    # RAM meter
    # ram_meter = get_meter_provider().get_meter("cpu-meter")

    # def ram_gauge_func(options):
    #     aggregate.measure()
    #     metrics = aggregate.get_metrics()
    #     aggregate_data = metrics["ram"]
    #     val = aggregate_data[len(aggregate_data)][2]

    #     yield Observation(val)

    # ram_gauge = ram_meter.create_observable_gauge(
    #     "ram_gauge",
    #     callbacks=[ram_gauge_func]
    # )


    # Disk meter
    # disk_meter = get_meter_provider().get_meter("disk-meter")

    # def disk_gauge_func(options):
    #     aggregate.measure()
    #     metrics = aggregate.get_metrics()
    #     aggregate_data = metrics["disk"]
    #     pair = aggregate_data[len(aggregate_data)][2]
    #     val = pair[0] + pair[1]

    #     yield Observation(val)

    # disk_gauge = disk_meter.create_observable_gauge(
    #     "disk_gauge",
    #     callbacks=[disk_gauge_func]
    # )


    # GPU meter
    # gpu_meter = get_meter_provider().get_meter("gpu-meter")

    # def gpu_gauge_func(options):
    #     aggregate.measure()
    #     metrics = aggregate.get_metrics()
    #     aggregate_data = metrics["gpu"]
    #     val = aggregate_data[len(aggregate_data)][2]

    #     yield Observation(val)

    # gpu_gauge = gpu_meter.create_observable_gauge(
    #     "gpu_gauge",
    #     callbacks=[gpu_gauge_func]
    # )