package main

import (
	"fmt"

	"github.com/goccy/go-json"
	"github.com/gofiber/fiber/v2"
)

type Application struct {
	AppName  string `json:"appName"`
	Language string `json:"language"`
}

type Applications struct {
	Applications []Application `json:"applications"`
}

func main() {
	app := fiber.New(fiber.Config{
		AppName:     "otcic-api",
		JSONEncoder: json.Marshal,
		JSONDecoder: json.Unmarshal,
	})

	api := app.Group("/api")

	api.Get("/apps", func(c *fiber.Ctx) error {
		result := Applications{}
		for i := 1; i < 4; i++ {
			appName := fmt.Sprintf("app-%d", i)
			result.Applications = append(result.Applications, Application{appName, "python"})
		}

		return c.JSON(result)
	})

	app.Listen(":54321")
}
