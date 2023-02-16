#include <Pdh.h>
#include <strsafe.h>

#include "otcic_gpu_win.hpp"

void cleanup(PDH_HQUERY query){
    if(query){
        PdhCloseQuery(query);
    }
}

BOOLEAN getPID_GPU_Available(DWORD pid){
    PDH_HQUERY hQuery = NULL;
    PDH_HCOUNTER hCounter = NULL;
    PDH_STATUS status = ERROR_SUCCESS;

    status = PdhOpenQueryW(NULL, NULL, &hQuery);
    cleanup(hQuery);

    return (status == ERROR_SUCCESS) ? TRUE : FALSE;
}

size_t getPID_GPU_Memory(DWORD pid){
    PDH_HQUERY hQuery = NULL;
    PDH_HCOUNTER hCounter = NULL;
    PDH_STATUS status = ERROR_SUCCESS;

    status = PdhOpenQueryW(NULL, NULL, &hQuery);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return 0ULL;
    }

    CHAR dst[64] = {"\0"};
    LPSTR counterPath = (LPSTR)dst;
    StringCbPrintfA(counterPath, (size_t)64, "\\GPU Process Memory(pid_%lu*)\\Local Usage", pid);

    status = PdhAddCounterA(hQuery, counterPath, NULL, &hCounter);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return 0ULL;
    }

    status = PdhCollectQueryData(hQuery);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return 0ULL;
    }

    PPDH_RAW_COUNTER pValue = NULL;
    LPDWORD counterType = NULL;
    status = PdhGetRawCounterValue(hCounter, counterType, pValue);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return 0ULL;
    }

    return pValue->FirstValue;
}

double getPID_GPU_Usage(DWORD pid){
    PDH_HQUERY hQuery = NULL;
    PDH_HCOUNTER hCounter = NULL;
    PDH_STATUS status = ERROR_SUCCESS;

    status = PdhOpenQueryW(NULL, NULL, &hQuery);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return -1.0;
    }

    CHAR dst[64] = {"\0"};
    LPSTR counterPath = (LPSTR)dst;
    StringCbPrintfA(counterPath, (size_t)64, "\\GPU Engine(pid_%lu*engtype_3D)\\Utilization Percentage", pid);

    status = PdhAddCounterA(hQuery, counterPath, NULL, &hCounter);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return -1.0;
    }

    status = PdhCollectQueryData(hQuery);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return -1.0;
    }

    status = PdhCollectQueryData(hQuery);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return -1.0;
    }

    PPDH_FMT_COUNTERVALUE pValue = NULL;
    LPDWORD counterType = NULL;
    status = PdhGetFormattedCounterValue(hCounter, PDH_FMT_DOUBLE, counterType, pValue);
    if(status != ERROR_SUCCESS){
        cleanup(hQuery);
        return -1.0;
    }

    return pValue->doubleValue;
}