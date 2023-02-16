#include <Pdh.h>
#include <d3d10.h>
#include "otcic_gpu_win.hpp"

// REWORK THIS CODE, ADD GPU STUFF

int getPID_GPU_Usage(void){
    PDH_HQUERY phQuery;
    PDH_STATUS status = ERROR_SUCCESS;
    status = PdhOpenQuery(NULL, NULL, &phQuery);

    // delete this, use another function, Pdh won't return GPU data
}