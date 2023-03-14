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

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from .aggregate import AggregateModel
# this is where all classes are going to be used and this specific module is imported

import requests
url = "http://api:54321/api/apps"

# delete this

INTERVAL_S = 3
aggregate = AggregateModel(INTERVAL_S)


def ram_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        aggregate.tracers["ram"].measure()
        return func(*args, **kwargs)
    return wrapper


def setup(service_name, cpu_model):
    # Send app name and language to API
    appObject = {
        'appName': service_name,
        'language': "python",
        'cpuModel': cpu_model
    }
    requests.post(url, appObject)

    # OpenTelemetry exporter setup
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    temporality_delta = {Counter: AggregationTemporality.DELTA}

    exporter = OTLPMetricExporter(
        endpoint="http://collector:4317",
        preferred_temporality=temporality_delta
    )

    # exporter = ConsoleMetricExporter(
    #     preferred_temporality=temporality_delta
    # )

    metric_reader = PeriodicExportingMetricReader(
        exporter,
        export_interval_millis=INTERVAL_S * 1000,
    )

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    set_meter_provider(meter_provider)

    meter = get_meter_provider().get_meter("metric-meter")

    def cpu_gauge_func(options):
        aggregate.measure()
        metrics = aggregate.get_metrics()
        aggregate_data = metrics["cpu"]
        val = aggregate_data[len(aggregate_data)-1][2]

        yield Observation(val)

    meter.create_observable_gauge(
        "cpu_gauge",
        callbacks=[cpu_gauge_func]
    )

    def ram_gauge_func(options):
        aggregate.measure()
        metrics = aggregate.get_metrics()
        aggregate_data = metrics["ram"]
        val = aggregate_data[len(aggregate_data)-1][2]

        yield Observation(val)

    meter.create_observable_gauge(
        "ram_gauge",
        callbacks=[ram_gauge_func]
    )

    def disk_gauge_func(options):
        aggregate.measure()
        metrics = aggregate.get_metrics()
        aggregate_data = metrics["disk"]
        pair = aggregate_data[len(aggregate_data)-1][2]
        val = pair[0] + pair[1]

        yield Observation(val)

    meter.create_observable_gauge(
        "disk_gauge",
        callbacks=[disk_gauge_func]
    )

    def gpu_gauge_func(options):
        aggregate.measure()
        metrics = aggregate.get_metrics()
        aggregate_data = metrics["gpu"]
        val = aggregate_data[len(aggregate_data)-1][2]

        yield Observation(val)

    meter.create_observable_gauge(
        "gpu_gauge",
        callbacks=[gpu_gauge_func]
    )

    def vram_gauge_func(options):
        aggregate.measure()
        metrics = aggregate.get_metrics()
        aggregate_data = metrics["vram"]
        val = aggregate_data[len(aggregate_data)-1][2]

        yield Observation(val)

    meter.create_observable_gauge(
        "vram_gauge",
        callbacks=[vram_gauge_func]
    )
