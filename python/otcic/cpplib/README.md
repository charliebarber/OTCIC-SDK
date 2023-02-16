# Compilation #

# Windows Library #

With export option on, this will compile the DLL with export functionality.
`-DOTCIC_GPU_WIN_EXPORT` - defines a value called `OTCIC_GPU_WIN_EXPORT`, used in compilation of .hpp file.

`g++ -c -DOTCIC_GPU_WIN_EXPORT otcic_gpu_win.cpp`

`g++ -shared -o otcic_gpu_win.dll otcic_gpu_win.o`

# Linux Library #

`g++ -c -o libotcicgpu.o libotcicgpu.cpp`

`gcc -shared -o libotcicgpu.so libotcicgpu.o`