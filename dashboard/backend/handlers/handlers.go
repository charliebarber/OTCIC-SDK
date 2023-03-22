package handlers

import (
	"github.com/gofiber/fiber/v2"

	"otcic/api/database"
	"otcic/api/models"
	"otcic/api/storage"
	"otcic/api/utils"
)

// Creates a new app in the local API storage
func AppCreate(c *fiber.Ctx) error {
	received := new(models.AppInfo)

	if err := c.BodyParser(received); err != nil {
		return c.Status(400).SendString(err.Error())
	}

	storage.Apps[received.AppName] = models.AppInfo{
		received.AppName,
		received.Language,
		received.CpuModel,
		received.Cores,
	}

	return c.SendString("Received app " + received.AppName)
}

func ListApps(c *fiber.Ctx) error {
	appsJson := models.Applications{}

	baseUrl := "http://prometheus:9090/api/v1/query?query="
	for name, info := range storage.Apps {
		if c.Query("metric") == "true" {
			sci := "n/a"
			cpu := database.FetchSingleMetric(baseUrl, name, "cpu_gauge")
			ram := database.FetchSingleMetric(baseUrl, name, "ram_gauge")
			disk := database.FetchSingleMetric(baseUrl, name, "disk_gauge")
			gpu := database.FetchSingleMetric(baseUrl, name, "gpu_gauge")
			vram := database.FetchSingleMetric(baseUrl, name, "vram_gauge")

			appsJson.Applications = append(appsJson.Applications, models.Application{
				name,
				info.Language,
				info.CpuModel,
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
				info.Language,
				info.CpuModel,
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

func RetrieveCI(c *fiber.Ctx) error {
	return c.JSON(utils.GetCarbonIntensity())
}

func RetrieveTDP(c *fiber.Ctx) error {
	cpuTdp := struct {
		Tdp int `json:"tdp"`
	}{
		Tdp: utils.GetCpuTdp(c.Query("cpuModel")),
	}

	return c.JSON(cpuTdp)
}

func RetrieveLoadAvg(c *fiber.Ctx) error {
	loadAvg := struct {
		LoadAvg float64 `json:"loadAvg"`
	}{
		LoadAvg: utils.GetLoadAvg(c.Query("appName")),
	}

	return c.JSON(loadAvg)
}

func RetrieveSCI(c *fiber.Ctx) error {
	sci := utils.CalculateSCI(c.Query("appName"))

	return c.JSON(sci)
}
