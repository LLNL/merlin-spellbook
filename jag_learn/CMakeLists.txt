cmake_minimum_required(VERSION 3.8.2)
project (basic_ensemble_support)

set(BLT_CXX_STD "c++11" CACHE PATH "")

################################
# Include blt
################################
if (NOT EXISTS ${PROJECT_SOURCE_DIR}/cmake/blt/SetupBLT.cmake)
    message(FATAL_ERROR 
"The BLT submodule is not present."
"If in git repository run the following two commands:\n"
"\n"
"git submodule init\n"
"git submodule update")

endif()
include(cmake/blt/SetupBLT.cmake)
include(cmake/SetupCompilerFlags.cmake)
include(cmake/SetupLibraries.cmake)

set(COLLECTOR_SOURCES  collector.cxx)
set(COLLECTOR_DEPENDS conduit hdf5)

blt_add_executable( NAME  collector
                  SOURCES ${COLLECTOR_SOURCES}
                  DEPENDS_ON ${COLLECTOR_DEPENDS}
                  OUTPUT_DIR bin )

