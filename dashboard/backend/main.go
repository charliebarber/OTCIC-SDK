package main

import (
	"github.com/goccy/go-json"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"

	"otcic/api/handlers"
	"otcic/api/models"
	"otcic/api/storage"
)

func main() {
	app := Setup()

	app.Listen(":54321")
}

func Setup() *fiber.App {
	app := fiber.New(fiber.Config{
		AppName:     "otcic-api",
		JSONEncoder: json.Marshal,
		JSONDecoder: json.Unmarshal,
	})

	storage.Apps = make(map[string]models.AppInfo)

	app.Use(cors.New())

	api := app.Group("/api")

	api.Post("/apps", handlers.AppCreate)

	api.Get("/apps", handlers.ListApps)

	api.Get("/app/:appName/:metric/:duration", handlers.RetrieveMetrics)

	api.Get("/ci", handlers.RetrieveCI)

	api.Get("/tdp", handlers.RetrieveTDP)

	api.Get("/loadAvg", handlers.RetrieveLoadAvg)

	api.Get("/sciScore", handlers.RetrieveSCI)

	return app
}
