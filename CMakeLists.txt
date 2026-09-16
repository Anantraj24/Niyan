cmake_minimum_required(VERSION 3.20)
project(NIYAM_X VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(NIYAM_ENABLE_CUDA "Enable CUDA acceleration backend" OFF)
option(NIYAM_BUILD_TESTS "Build test suite" ON)

if(NIYAM_ENABLE_CUDA)
    enable_language(CUDA)
    add_compile_definitions(NIYAM_HAS_CUDA=1)
endif()

add_subdirectory(core)
add_subdirectory(verifier)
