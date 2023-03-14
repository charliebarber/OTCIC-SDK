package utils

import (
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/goccy/go-json"
	"otcic/api/models"
)

func GetCarbonIntensity() models.CIIntensity {
	baseUrl := "http://api.carbonintensity.org.uk"
	url := baseUrl + "/intensity"

	ciReponse := models.CIResponse{}

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

	jsonErr := json.Unmarshal(body, &ciReponse)
	if jsonErr != nil {
		log.Print(jsonErr)
	}

	return ciReponse.Data[0].Intensity
}
