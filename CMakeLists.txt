cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 14)

include_directories(${PROJECT_SOURCE_DIR}/inc)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

# REST_PATH
IF (NOT DEFINED REST_PATH)
    IF (DEFINED ENV{REST_PATH})
        set(REST_PATH $ENV{REST_PATH})
    ELSE ()
        message(FATAL_ERROR "ERROR ::: REST_PATH must be defined as an environment variable and point to REST install directory")
        return()
    ENDIF ()
ENDIF ()
set(CMAKE_INSTALL_PREFIX ${REST_PATH})
message(STATUS "Using REST PATH: " ${REST_PATH})

# ROOT
include(FindRoot)

set(lnklib -L${REST_PATH}/lib/ -lRestTools -lRestCore -lRestEvents -lRestMetadata ${ROOT_LIBRARIES} -lboost_system -lboost_program_options -lboost_filesystem -lGui -lEve -lRGL -lGeom -lGdml -lMinuit)

include_directories(${ROOT_INCLUDE_DIRS})
include_directories(${REST_PATH}/include)


add_executable(restSQL restSQL.cpp inc/TRestSql.h src/TRestSql.cxx)

target_link_libraries(restSQL ${lnklib})
