package utils

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"time"

	"encoding/json"
	"otcic/api/database"
	"otcic/api/models"

	"github.com/lithammer/fuzzysearch/fuzzy"

	"embed"
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

	body, readErr := io.ReadAll(res.Body)
	if readErr != nil {
		log.Print(readErr)
	}

	jsonErr := json.Unmarshal(body, &ciReponse)
	if jsonErr != nil {
		log.Print(jsonErr)
	}

	return ciReponse.Data[0].Intensity
}

//go:embed tdp.json
var f embed.FS

func readCpuTdps() []models.CpuData {

	content, err := f.ReadFile("tdp.json")
	if err != nil {
		log.Fatal("Error when opening file: ", err)
	}

	cpuDataArr := []models.CpuData{}

	err = json.Unmarshal(content, &cpuDataArr)
	if err != nil {
		log.Fatal("Error unmarshalling: ", err)
	}

	return cpuDataArr
}

func GetCpuTdp(cpuModel string) int {
	cpuTdps := readCpuTdps()

	closestDistance := 64
	var closestMatch models.CpuData
	for _, cpu := range cpuTdps {
		fmt.Println("CPU: ", cpu.Model, "TDP: ", cpu.TDP)
		rank := fuzzy.LevenshteinDistance(cpu.Model, cpuModel)
		if rank >= 0 && rank < closestDistance {
			closestMatch = cpu
			closestDistance = rank
		}
	}

	fmt.Println("Closest match to ", cpuModel, "was ", closestMatch.Model, "with TDP", closestMatch.TDP)
	fmt.Println("Distance was", closestDistance)

	return closestMatch.TDP
}

func GetLoadAvg(app string) float64 {
	baseUrl := "http://prometheus:9090/api/v1/query?query="
	resultValue := database.FetchSingleMetric(baseUrl, app, "loadavg_gauge")
	val, err := strconv.ParseFloat(resultValue.Val, 64)
	if err != nil {
		log.Fatal("Error converting load avg", err)
	}
	return val
}
