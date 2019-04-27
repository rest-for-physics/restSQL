# Inspired from "FindROOT.cmake"
# Created by lobis on 4/27/19.
#
# - Finds REST instalation
# This module sets up REST information
# It defines:
# REST_FOUND          If the REST package is found
# REST_INCLUDE_DIRS   PATH to the include directory
# REST_LIBRARIES      Most common libraries
# REST_LIBRARY_DIR    PATH to the library directory
# REST_BIN_DIR	      PATH to the excutables directory TODO: include this

# REST_PATH is equivalent of ROOTSYS for ROOT (REST installation directory)
# REST_PATH should be defined as environment variable via "thisREST.sh" script
# If not found add this script to your .bashrc
IF (NOT DEFINED REST_PATH)
    message(STATUS "REST_PATH not defined in CMake (-DREST_PATH=your_REST_PATH not used). Using environment variable REST_PATH: ${REST_PATH}")
    set(REST_PATH $ENV{REST_PATH})
else()
    message(STATUS "REST_PATH: ${REST_PATH} defined in CMake (-DREST_PATH=your_REST_PATH was used)")
ENDIF ()

#find_program(REST_CONFIG_EXECUTABLE rest-config PATHS ${REST_PATH}/bin)
find_program(REST_CONFIG_EXECUTABLE rest-config PATHS ${REST_PATH}/bin NO_SYSTEM_ENVIRONMENT_PATH)

message(STATUS "REST_CONFIG_EXECUTABLE: ${REST_CONFIG_EXECUTABLE}")

if (NOT REST_CONFIG_EXECUTABLE)
    set(REST_FOUND FALSE)
else ()
    set(REST_FOUND TRUE)

    # get REST version
    execute_process(
            COMMAND ${REST_CONFIG_EXECUTABLE} --version
            OUTPUT_VARIABLE REST_VERSION
            OUTPUT_STRIP_TRAILING_WHITESPACE)

    execute_process(
            COMMAND ${REST_CONFIG_EXECUTABLE} --incdir
            OUTPUT_VARIABLE REST_INCLUDE_DIRS
            OUTPUT_STRIP_TRAILING_WHITESPACE)

    execute_process(
            COMMAND ${REST_CONFIG_EXECUTABLE} --libs
            OUTPUT_VARIABLE REST_LIBRARIES
            OUTPUT_STRIP_TRAILING_WHITESPACE)

    # should be implemented in rest-config not manually
    set(REST_BIN_DIR ${REST_PATH}/bin)

    set(REST_LIBRARY_DIR ${REST_PATH}/lib)
    set(REST_INCLUDE_DIR ${REST_INCLUDE_DIRS})

    if (NOT REST_FIND_QUIETLY)
        message(STATUS "Found REST ${REST_VERSION} in ${REST_PATH}")
    endif ()
endif ()

if (NOT REST_FOUND)
    if (REST_FIND_REQUIRED)
        message(FATAL_ERROR "REST required, but not found")
    endif (REST_FIND_REQUIRED)
endif ()