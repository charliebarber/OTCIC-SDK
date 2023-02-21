from setuptools import setup

setup(
    name = "otcic",
    packages = ["otcic"],
    version = "0.0.1",
    install_requires = [
        "gpustat>=1.0.0",
        "opentelemetry-api>=1.15.0",
        "opentelemetry-exporter-otlp>=1.15.0",
        "opentelemetry-exporter-otlp-proto-grpc>=1.15.0",
        "opentelemetry-proto>=1.15.0",
        "opentelemetry-sdk>=1.15.0",
        "psutil>=5.9.4"
    ],
    python_requires = ">=3.10"
)