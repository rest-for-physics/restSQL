cmake_minimum_required(VERSION 2.8)
project(restSQL)

set(CMAKE_CXX_STANDARD 14)

# necessary to use the scripts in "cmake" folder
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

# include 'inc' and 'src' directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/inc ${CMAKE_CURRENT_SOURCE_DIR}/src)

# ROOT
set(ROOT_FIND_REQUIRED TRUE)
include(FindRoot)
message(STATUS "ROOT_INCLUDE_DIRS: ${ROOT_INCLUDE_DIRS}")
include_directories(${ROOT_INCLUDE_DIRS})
message(STATUS "ROOT_LIBRARIES: ${ROOT_LIBRARIES}")

# REST
set(REST_FIND_REQUIRED TRUE)
# minimum required version
set(REST_MINIMUM_REQUIRED_VERSION 2.2.10)
include(FindRest)
message(STATUS "REST_INCLUDE_DIRS: ${REST_INCLUDE_DIRS}")
include_directories(${REST_INCLUDE_DIRS})
message(STATUS "REST_LIBRARIES: ${REST_LIBRARIES}")

set(lnklib ${REST_LIBRARIES} ${ROOT_LIBRARIES})

#add_executable(restSQL restSQL.cpp inc/TRestSql.h src/TRestSql.cxx)
add_executable(restSQL restSQL.cpp)

message(STATUS "libraries to link: ${lnklib}")
target_link_libraries(restSQL ${lnklib})