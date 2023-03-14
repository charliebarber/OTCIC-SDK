package database

import (
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/goccy/go-json"
	"otcic/api/models"
)

func FetchSingleMetric(baseUrl string, appName string, metric string) models.Value {
	promResponse := models.PromQLResponse{}

	url := baseUrl + metric + "{job=\"" + appName + "\"}"

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

	return promResponse.ResponseData.ResultData[0].ResultValue
}

func FetchMetrics(baseUrl string, appName string, metric string, duration string) models.PromQLResultData {
	promResponse := models.PromQLResponse{}

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
