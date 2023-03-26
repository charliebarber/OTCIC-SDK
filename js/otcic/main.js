const otel = require("@opentelemetry/api");
const {
  MeterProvider,
  PeriodicExportingMetricReader,
  ConsoleMetricExporter,
} = require("@opentelemetry/sdk-metrics");
const { Resource } = require("@opentelemetry/resources");
const {
  SemanticResourceAttributes,
} = require("@opentelemetry/semantic-conventions");
const {
  OTLPMetricExporter,
} = require("@opentelemetry/exporter-metrics-otlp-grpc");
const axios = require("axios").default;
const os = require("os");

const url = "http://api:54321/api/apps";
const INTERVAL = 3;

let bytesToMB = 1 / (1024 * 1024)

function getCpuPercent() {
  let startUsage = process.cpuUsage();
  let startTime = process.hrtime.bigint();

  // now given in milliseconds
  const now = Date.now();
  // let cpu spin for 100ms
  while (Date.now() - now < 100);

  let endTime = process.hrtime.bigint();
  // given in nanoseconds 1000 ns = 1 micros
  let elapsedTime = endTime - startTime;
  // 1,000,000 nano seconds = 1ms
  let elapsedTimeMS = Number(1000000n * elapsedTime);
  // given in microseconds, 1000 micro = 1 ms
  let elapsedUsage = process.cpuUsage(startUsage);
  let usageMS = Object.values(elapsedUsage).map((usage) => usage * 1000);

  let cpuPercent = (100 * (usageMS[0] + usageMS[1])) / elapsedTimeMS;

  return cpuPercent;
}

let lastCpuPercent = 0.0;

function setup(serviceName) {
  axios
    .post(url, {
      appName: serviceName,
      language: "JavaScript",
      cpuModel: os.cpus()[0].model,
      cores: os.cpus().length,
    })
    .catch((err) => {
      console.log("Error posting new app to API: ", err);
    });

  const metricExporter = new OTLPMetricExporter({
    url: "http://collector:4317",
  });

  const meterProvider = new MeterProvider({
    resource: new Resource({
      [SemanticResourceAttributes.SERVICE_NAME]: serviceName,
    }),
  });

  const metricReader = new PeriodicExportingMetricReader({
    exporter: metricExporter,
    exportIntervalMillis: INTERVAL * 1000,
  });

  meterProvider.addMetricReader(metricReader);

  const meter = meterProvider.getMeter("metric-meter");

  // CPU Meter readings
  let prevCpuTime = process.cpuUsage();

  // Gauge to monitor CPU use by CPU time used by process
  const cpuGauge = meter.createObservableGauge("cpu_gauge", {
    description: "CPU time",
    unit: "microseconds",
  });

  cpuGauge.addCallback((result) => {
    // User CPU time and System CPU time
    // User measures the time taken by app
    let percent = getCpuPercent();

    result.observe(percent);
  });

  // CPU Load avg - unix specific
  const loadAvgGauge = meter.createObservableGauge("loadavg_gauge", {
    description: "Load Average 1m",
    unit: "load",
  });

  loadAvgGauge.addCallback((result) => {
    const [LoadAvg1m, LoadAvg5m, LoadAvg15m] = os.loadavg();
    result.observe(LoadAvg1m);
  });

  // Gauge to monitor memory use as a %
  const memoryUsageGauge = meter.createObservableGauge("ram_gauge", {
    description: "Memory usage",
    unit: "%",
  });

  memoryUsageGauge.addCallback((result) => {
    const { heapTotal, heapUsed } = process.memoryUsage();
    const totalMemory = os.totalmem();
    const percent = heapTotal / totalMemory;
    result.observe(heapUsed * bytesToMB);
  });

  // Disk gauge
  const diskGauge = meter.createObservableGauge("disk_gauge", {});

  diskGauge.addCallback((result) => {
    result.observe(0);
  });

  // GPU gauge
  const gpuGauge = meter.createObservableGauge("gpu_gauge", {});

  gpuGauge.addCallback((result) => {
    result.observe(0);
  });

  // VRAM gauge
  const vramGauge = meter.createObservableGauge("vram_gauge", {});

  vramGauge.addCallback((result) => {
    result.observe(0);
  });

  // Set this MeterProvider to be global to the app being instrumented.
  otel.metrics.setGlobalMeterProvider(meterProvider);
}

module.exports = {
  setup,
  getCpuPercent,
};
