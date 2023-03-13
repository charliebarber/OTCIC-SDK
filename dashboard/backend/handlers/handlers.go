package handlers

import (
	"github.com/gofiber/fiber/v2"

	"otcic/api/database"
	"otcic/api/models"
	"otcic/api/storage"
)

// Creates a new app in the local API storage
func AppCreate(c *fiber.Ctx) error {
	received := new(models.Application)

	if err := c.BodyParser(received); err != nil {
		return c.Status(400).SendString(err.Error())
	}

	storage.Apps[received.AppName] = received.Language

	return c.SendString("Received app " + received.AppName)
}

func ListApps(c *fiber.Ctx) error {
	appsJson := models.Applications{}

	baseUrl := "http://prometheus:9090/api/v1/query?query="
	for name, language := range storage.Apps {
		if c.Query("metric") == "true" {
			sci := "n/a"
			cpu := database.FetchSingleMetric(baseUrl, name, "cpu_gauge")
			ram := database.FetchSingleMetric(baseUrl, name, "ram_gauge")
			disk := database.FetchSingleMetric(baseUrl, name, "disk_gauge")
			gpu := database.FetchSingleMetric(baseUrl, name, "gpu_gauge")
			vram := database.FetchSingleMetric(baseUrl, name, "vram_gauge")

			appsJson.Applications = append(appsJson.Applications, models.Application{
				name,
				language,
				sci,
				cpu.Val,
				ram.Val,
				disk.Val,
				gpu.Val,
				vram.Val,
			})
		} else {
			appsJson.Applications = append(appsJson.Applications, models.Application{
				name,
				language,
				"",
				"",
				"",
				"",
				"",
				"",
			})
		}
	}

	return c.JSON(appsJson)
}

// Retrieve the metrics of a specific app
func RetrieveMetrics(c *fiber.Ctx) error {
	baseUrl := "http://prometheus:9090/api/v1/query?query="

	if _, ok := storage.Apps[c.Params("appName")]; !ok {
		return c.Status(404).SendString("App does not exist")
	}

	var result models.PromQLResultData
	switch c.Params("metric") {
	case "cpu":
		result = database.FetchMetrics(baseUrl, c.Params("appName"), "cpu_gauge", c.Params("duration"))
	case "ram":
		result = database.FetchMetrics(baseUrl, c.Params("appName"), "ram_gauge", c.Params("duration"))
	case "disk":
		result = database.FetchMetrics(baseUrl, c.Params("appName"), "disk_gauge", c.Params("duration"))
	case "gpu":
		result = database.FetchMetrics(baseUrl, c.Params("appName"), "gpu_gauge", c.Params("duration"))
	case "vram":
		result = database.FetchMetrics(baseUrl, c.Params("appName"), "vram_gauge", c.Params("duration"))
	}

	return c.JSON(result)
}
