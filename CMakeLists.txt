cmake_minimum_required(VERSION 2.8)
project(restSQL)

set(CMAKE_CXX_STANDARD 14)

# necessary to use the scripts in "cmake" folder
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

# include 'inc' and 'src' directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/inc ${CMAKE_CURRENT_SOURCE_DIR}/src)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/utils/inc ${CMAKE_CURRENT_SOURCE_DIR}/utils/src)

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

# database libraries
SET(LD_DEBUG ALL)
set(DATABASE_LIBRARIES "")
if (SQLITE)
    # TODO: sqlite/lib should be added to LD_LIBRARY_PATH so -L option is not needed
    set(SQLITE_PATH /home/lobis/apps/sqlite/)
    set(DATABASE_LIBRARIES "${DATABASE_LIBRARIES}-L${SQLITE_PATH}/lib -lsqlite3")
    include_directories(${SQLITE_PATH}/include)
endif()
# TODO: add postgresql as option
message(STATUS "DATABASE LIBRARIES: ${DATABASE_LIBRARIES}")

set(lnklib ${REST_LIBRARIES} ${ROOT_LIBRARIES} ${DATABASE_LIBRARIES})

add_executable(restSQL restSQL.cpp inc/TRestSql.h src/TRestSql.cxx utils/inc/sha1.h utils/src/sha1.cxx)

message(STATUS "libraries to link: ${lnklib}")
target_link_libraries(restSQL ${lnklib})