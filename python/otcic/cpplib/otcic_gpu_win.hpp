#ifndef OTCIC_GPU_WIN_INCLUDED
    #define OTCIC_GPU_WIN_INCLUDED

    // use tag -DOTCIC_GPU_WIN_EXPORT when compiling with g++
    #ifdef OTCIC_GPU_WIN_EXPORT
        #define OTCIC_GPU_WIN_API __declspec(dllexport)
    #else
        #define OTCIC_GPU_WIN_API __declspec(dllimport)
    #endif

    #ifdef __cplusplus
    extern "C" {
    #endif

    OTCIC_GPU_WIN_API BOOLEAN getPID_GPU_Available(DWORD pid);
    OTCIC_GPU_WIN_API size_t getPID_GPU_Memory(DWORD pid);
    OTCIC_GPU_WIN_API double getPID_GPU_Usage(DWORD pid);

    #ifdef __cplusplus
    }
    #endif

#endif
