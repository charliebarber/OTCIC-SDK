package main

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/charliebarber/OTCIC-SDK/api/models"
	"github.com/charliebarber/OTCIC-SDK/api/storage"
	"github.com/charliebarber/OTCIC-SDK/api/utils"
)

func TestAppCreate(t *testing.T) {
	app := Setup()

	tests := []struct {
		name         string
		reqBody      string
		expectedRes  string
		expectedCode int
	}{
		{
			name: "create a new app",
			reqBody: `{
				"appName": "myApp",
				"language": "go",
				"cpuModel": "Intel Core i5",
				"cores": 4
			}`,
			expectedRes:  "Received app myApp",
			expectedCode: 200,
		},
		{
			name: "create a new app with missing fields",
			reqBody: `{
				"appName": "myApp2",
				"cpuModel": "AMD Ryzen 7"
			}`,
			expectedRes:  "Received app myApp2",
			expectedCode: 200,
		},
		{
			name:         "create a new app with invalid JSON",
			reqBody:      `{"appName": "myApp", "language": "go", "cpuModel": `,
			expectedRes:  "Error parsing request body",
			expectedCode: 400,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodPost, "/api/apps", strings.NewReader(tt.reqBody))
			req.Header.Set("Content-Type", "application/json")

			res, err := app.Test(req, -1)
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedCode, res.StatusCode)

			resBody, _ := io.ReadAll(res.Body)
			if err != nil {
				t.Error(err)
			}
			body := string(resBody)
			assert.Equal(t, body, tt.expectedRes, "Both response bodies should be equal")

			if tt.expectedRes == "Received app "+body {
				if _, ok := storage.Apps[body]; !ok {
					t.Errorf("App not created. Expected: %s, got: %v", tt.expectedRes, storage.Apps[body])
				}
			}
		})
	}
}

func TestListApps(t *testing.T) {
	app := Setup()

	testApp := models.AppInfo{
		AppName:  "myApp",
		Language: "go",
		CpuModel: "Intel Core i5",
		Cores:    4,
	}

	// Create a sample app to list
	appReq := httptest.NewRequest(http.MethodPost, "/api/apps", strings.NewReader(`{
		"appName": "myApp",
		"language": "go",
		"cpuModel": "Intel Core i5",
		"cores": 4
	}`))
	appReq.Header.Set("Content-Type", "application/json")
	appRes, err := app.Test(appReq, -1)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, appRes.StatusCode)

	tests := []struct {
		name         string
		expectedRes  string
		expectedCode int
	}{
		{
			name:         "list all apps",
			expectedRes:  `{"applications":[{"appName":"myApp","language":"go","cpuModel":"Intel Core i5","sci":"","cpuVal":"","ramVal":"","diskVal":"","gpuVal":"","vramVal":""}]}`,
			expectedCode: http.StatusOK,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodGet, "/api/apps", nil)

			res, err := app.Test(req, -1)
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedCode, res.StatusCode)

			resBody, _ := io.ReadAll(res.Body)
			if err != nil {
				t.Error(err)
			}
			body := string(resBody)
			assert.Equal(t, tt.expectedRes, body, "Both response bodies should be equal")

			// test if JSON demarshals to model correctly
			var applications models.Applications
			err = json.Unmarshal(resBody, &applications)
			if err != nil {
				t.Fatal(err)
			}

			// Check that the retrieved app matches the test app
			assert.Equal(t, testApp.AppName, applications.Applications[0].AppName)
			assert.Equal(t, testApp.Language, applications.Applications[0].Language)
			assert.Equal(t, testApp.CpuModel, applications.Applications[0].CpuModel)
			assert.Equal(t, "", applications.Applications[0].Sci)
			assert.Equal(t, "", applications.Applications[0].CpuVal)
			assert.Equal(t, "", applications.Applications[0].RamVal)
			assert.Equal(t, "", applications.Applications[0].DiskVal)
			assert.Equal(t, "", applications.Applications[0].GpuVal)
			assert.Equal(t, "", applications.Applications[0].VramVal)
		})
	}
}

// white box testing using mock
func TestRetrieveCI(t *testing.T) {
	app := Setup()

	// create a mock response
	mockCIIntensity := models.CIIntensity{
		Forecast: 0,
		Actual:   0,
	}

	// Set the mock response
	utils.GetCarbonIntensity = func() models.CIIntensity {
		return mockCIIntensity
	}

	// Create a request
	req, err := http.NewRequest(http.MethodGet, "/api/ci", nil)

	res, err := app.Test(req, -1)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, res.StatusCode)

	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		t.Fatal(err)
	}

	// Check the response body contains the expected data
	var resCI models.CIIntensity
	err = json.Unmarshal(resBody, &resCI)
	if err != nil {
		t.Fatal(err)
	}

	assert.Equal(t, mockCIIntensity, resCI)
}

func TestRetrieveTDP(t *testing.T) {
	app := Setup()

	// create a mock response
	mockTDP := struct {
		Tdp int
	}{
		Tdp: 65,
	}

	// Create a request
	req, err := http.NewRequest(http.MethodGet, "/api/tdp", nil)
	if err != nil {
		t.Fatal(err)
	}

	query := url.Values{}
	query.Add("cpuModel", "Ryzen 5 3600")
	req.URL.RawQuery = query.Encode()

	res, err := app.Test(req, -1)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, res.StatusCode)

	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		t.Fatal(err)
	}

	// Check the response body contains the expected data
	var resTDP struct {
		Tdp int
	}
	err = json.Unmarshal(resBody, &resTDP)
	if err != nil {
		t.Fatal(err)
	}

	assert.Equal(t, mockTDP, resTDP)
}
