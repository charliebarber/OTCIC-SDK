#ifndef OTCIC_GPU_WIN_INCLUDED
    #define OTCIC_GPU_WIN_INCLUDED

    #ifdef __cplusplus
        extern "C" {
    #endif

    // use tag -DOTCIC_GPU_WIN_EXPORT when compiling with g++
    #ifdef OTCIC_GPU_WIN_EXPORT
        #define OTCIC_GPU_WIN_API __declspec(dllexport)
    #else
        #define OTCIC_GPU_WIN_API __declspec(dllimport)
    #endif

    BOOLEAN OTCIC_GPU_WIN_API getPID_GPU_Available(DWORD pid);
    size_t OTCIC_GPU_WIN_API getPID_GPU_Memory(DWORD pid);
    double OTCIC_GPU_WIN_API getPID_GPU_Usage(DWORD pid);

    #ifdef __cplusplus
        }
    #endif

#endif
