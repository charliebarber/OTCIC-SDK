# OTCIC SDK

The Open Telemetry Carbon Intensity Calculator SDK (OTCIC SDK) is a project between [UCL](https://www.ucl.ac.uk/) Computer Science students
and [NTT Data](https://www.nttdata.com/global/en) who are working on a calculator for Software Carbon Intensity.
Our role as students is to create an SDK to feed data into this calculator.
[Software Carbon Intensity](https://greensoftware.foundation/articles/software-carbon-intensity-crafting-a-standard) is a term
coined by the [Green Software Foundation](https://greensoftware.foundation/), of which NTT data is a member, aiming to measure
the carbon impact of software systems.

## Demonstration

The project uses Open Telemetry API to handle the gathered data and sends it to Open Telemetry Collector. The Collector is then capable of sending the recordings to a back end or dashboard.

### Docker Collector setup

To start the Collector with Docker run:
```
cd ./docker && docker-compose down && docker-compose up
```

To stop the Docker container:
```
cd ./docker && docker-compose down
```

### JavaScript

To run the example JavaScript application, run:
```
node --require './js/instrumentation.js' js/app.js
```

The application is a simple Express app listening for HTTP requests. `instrumentation.js` then listens for CPU and RAM metrics every 3 seconds.
