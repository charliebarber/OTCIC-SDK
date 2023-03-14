package models

import (
	"fmt"
	"github.com/goccy/go-json"
)

// App structs

type Application struct {
	AppName  string `json:"appName"`
	Language string `json:"language"`
	Sci      string `json:"sci"`
	CpuVal   string `json:"cpuVal"`
	RamVal   string `json:"ramVal"`
	DiskVal  string `json:"diskVal"`
	GpuVal   string `json:"gpuVal"`
	VramVal  string `json:"vramVal"`
}

type Applications struct {
	Applications []Application `json:"applications"`
}

// Structs for PromQL database queries

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
	ResultValue  Value                  `json:"value"`
}

type PromQLResultDataSingular struct {
	ResultMetric PromQLResultMetricData `json:"metric"`
	ResultValue  Value                  `json:"value"`
}

type PromQLResultMetricData struct {
	ResultName string `json:"__name__"`
	ResultJob  string `json:"job"`
}

// Unmarshalling model code

func (value *Value) UnmarshalJSON(data []byte) error {
	var tmp []interface{}
	if err := json.Unmarshal(data, &tmp); err != nil {
		return err
	}
	value.Time = fmt.Sprintf("%f", tmp[0])
	value.Val = fmt.Sprintf("%s", tmp[1])

	return nil
}

// Carbon intensity models

type CIResponse struct {
	Data []CIData `json:"data"`
}

type CIData struct {
	Intensity CIIntensity `json:"intensity"`
}

type CIIntensity struct {
	Forecast int `json:"forecast"`
	Actual   int `json:"actual"`
}
