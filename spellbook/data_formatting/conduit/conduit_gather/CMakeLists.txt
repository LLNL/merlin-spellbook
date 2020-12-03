###############################################################################

cmake_minimum_required(VERSION 3.0)

################################
# Conduit Gather
################################

project(conduit_gather VERSION "0.0.1")


################################ 
# Build Options
################################
option(ENABLE_TESTS       "Build conduit tests"         OFF)
#option(ENABLE_EXAMPLES    "Build Examples"              ON)
#option(ENABLE_DOCS        "Build conduit documentation" ON)

option(ENABLE_MPI         "Build MPI Support"           ON)


# don't use BLT's all warnings feature
set(ENABLE_ALL_WARNINGS OFF CACHE BOOL "")

################################
# Init BLT
################################
# This also includes 
# Conduit's BLT defaults
include(cmake/SetupBLT.cmake)

################################
# Set some standard cmake opts
################################
include(cmake/CMakeBasics.cmake)

################################
# Setup 3rd Party Libs
################################
if(DEFINED conduit_DIR)
   include(${conduit_DIR}/ConduitConfig.cmake)
   blt_register_library(NAME conduit
                        INCLUDES "${conduit_DIR}/../../include"
                        LIBRARIES conduit conduit_relay conduit_relay_mpi 
                        )
endif()
#include(cmake/Setup3rdParty.cmake)

################################
# Setup our actual code
################################
add_subdirectory(src)


################################
# Add our tests
################################
if(ENABLE_TESTS)
    add_subdirectory(tests)
else()
    message(STATUS "Skipping test targets (ENABLE_TESTS = OFF)")
endif()


################################
# Create CMake importable
# exports for all of our targets
################################
# install exports to comply with standard find_package search path expectations
#install(EXPORT conduit DESTINATION lib/cmake/conduit)
# also install to support our old export directory layout 
# (preserving for now to avoid issues with downstream packages using old layout)
#install(EXPORT conduit DESTINATION lib/cmake)

