package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

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

type Metrics struct {
	Values []Value `json:"values"`
}

type Value struct {
	Time string `json:"time"`
	Val  string `json:"val"`
}

type PromQLResponse struct {
	ResponseStatus string     `json:"status"`
	ResponseData   PromQLData `json:"data"`
}

type PromQLData struct {
	ResultType string             `json:"resultType"`
	ResultData []PromQLResultData `json:"result"`
}

type PromQLResultData struct {
	ResultMetric PromQLResultMetricData `json:"metric"`
	ResultValues []Value                `json:"values"`
}

type PromQLResultMetricData struct {
	ResultName string `json:"__name__"`
	ResultJob  string `json:"job"`
}

func (value *Value) UnmarshalJSON(data []byte) error {
	var tmp []interface{}
	if err := json.Unmarshal(data, &tmp); err != nil {
		return err
	}
	value.Time = fmt.Sprintf("%f", tmp[0])
	value.Val = fmt.Sprintf("%s", tmp[1])

	return nil
}

func fetchMetrics(baseUrl string, appName string, metric string, duration string) PromQLResultData {
	promResponse := PromQLResponse{}

	url := baseUrl + metric + "{job=\"" + appName + "\"}[" + duration + "]"

	client := http.Client{
		Timeout: time.Second * 3,
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		log.Print(err)
	}

	req.Header.Set("User-Agent", "otcic-api")

	res, getErr := client.Do(req)
	if getErr != nil {
		log.Print(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Print(readErr)
	}

	jsonErr := json.Unmarshal(body, &promResponse)
	if jsonErr != nil {
		log.Print(jsonErr)
	}

	return promResponse.ResponseData.ResultData[0]
}

func main() {
	app := fiber.New(fiber.Config{
		AppName:     "otcic-api",
		JSONEncoder: json.Marshal,
		JSONDecoder: json.Unmarshal,
	})

	api := app.Group("/api")

	apps := make(map[string]string)

	api.Post("/apps", func(c *fiber.Ctx) error {
		received := new(Application)

		if err := c.BodyParser(received); err != nil {
			return c.Status(400).SendString(err.Error())
		}

		apps[received.AppName] = received.Language

		return c.SendString("Received app " + received.AppName)
	})

	api.Get("/apps", func(c *fiber.Ctx) error {
		appsJson := Applications{}

		for name, language := range apps {
			appsJson.Applications = append(appsJson.Applications, Application{name, language})
		}

		return c.JSON(appsJson)
	})

	api.Get("/app/:appName/:metric/:duration", func(c *fiber.Ctx) error {
		baseUrl := "http://prometheus:9090/api/v1/query?query="

		if _, ok := apps[c.Params("appName")]; !ok {
			return c.Status(404).SendString("App does not exist")
		}

		var result PromQLResultData
		switch c.Params("metric") {
		case "cpu":
			result = fetchMetrics(baseUrl, c.Params("appName"), "cpu_gauge", c.Params("duration"))
		case "ram":
			result = fetchMetrics(baseUrl, c.Params("appName"), "ram_gauge", c.Params("duration"))
		case "disk":
			result = fetchMetrics(baseUrl, c.Params("appName"), "disk_gauge", c.Params("duration"))
		case "gpu":
			result = fetchMetrics(baseUrl, c.Params("appName"), "gpu_gauge", c.Params("duration"))
		}

		return c.JSON(result)
	})

	app.Listen(":54321")
}
