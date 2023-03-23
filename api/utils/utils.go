package utils

import (
	"io"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"

	"encoding/json"
	"github.com/charliebarber/OTCIC-SDK/api/database"
	"github.com/charliebarber/OTCIC-SDK/api/models"
	"github.com/charliebarber/OTCIC-SDK/api/storage"

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
		rank := fuzzy.LevenshteinDistance(cpu.Model, cpuModel)
		if rank >= 0 && rank < closestDistance {
			closestMatch = cpu
			closestDistance = rank
		}
	}

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

func CalculateSCI(appName string) models.SCIResponse {
	baseUrl := "http://prometheus:9090/api/v1/query?query="

	// CPU: n cores * TDP * log(loadCPU * 100)/log(200)
	loadAvg := GetLoadAvg(appName)
	appInfo := storage.Apps[appName]
	tdp := GetCpuTdp(appInfo.CpuModel)
	cores := appInfo.Cores

	cpuScore := (float64(cores) * float64(tdp) * math.Log10(loadAvg*100)) / math.Log10(200)
	cpuRes := models.CPUResponse{
		loadAvg,
		tdp,
		cores,
		cpuScore,
	}

	// PRAM = 0.3725 W/GB x memAlloc
	mem := database.FetchMetricAverage(baseUrl, appName, "ram_gauge", "5m")
	memVal, err := strconv.ParseFloat(mem.Val, 64)
	if err != nil {
		log.Fatal("Error converting mem val", err)
	}
	memScore := 0.3725 * (memVal / 1024.0)
	memRes := models.MemResponse{
		memVal,
		memScore,
	}

	// Per HDD: PHDD= 0.65 Wh/TBh x MemSize
	disk := database.FetchMetricAverage(baseUrl, appName, "disk_gauge", "5m")
	diskVal, err := strconv.ParseFloat(disk.Val, 64)
	if err != nil {
		log.Fatal("Error converting disk val", err)
	}
	diskScore := 0.65 * (diskVal / 1024.0)
	diskRes := models.DiskResponse{
		diskVal,
		diskScore,
	}

	return models.SCIResponse{
		int(math.Round(cpuScore + memScore + diskScore)),
		cpuRes,
		memRes,
		diskRes,
	}
}
