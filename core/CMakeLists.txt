add_executable(niyam
    main.cpp
)

target_include_directories(niyam PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

if(NIYAM_ENABLE_CUDA)
    target_sources(niyam PRIVATE cuda/cuda_kernel.cu)
endif()
