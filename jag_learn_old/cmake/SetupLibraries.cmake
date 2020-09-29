# Find the version of conduit compatible with current python
execute_process(COMMAND python -c "import sys;t='{v[0]}_{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)" OUTPUT_VARIABLE PYVD )
message(STATUS "PYTHON VERSION is ${PYVD}")
set(PYV "py${PYVD}" CACHE PATH "")
set(CONDUIT_DIR "/collab/usr/gapps/merlin/build/conduit/install-$ENV{SYS_TYPE}_${PYV}" CACHE PATH "")
message(STATUS "CONDUIT DIRECTORY is ${CONDUIT_DIR}")

# Search through conduit's cmake files to find the version of hdf5 used
# Extract that line, stash in a new cmake file and then include it;
# This is easier than wrestling with awk and sed from within cmake

execute_process(COMMAND grep CONDUIT_HDF5_DIR "${CONDUIT_DIR}/lib/cmake/ConduitConfig.cmake" OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/hdf5_lib.cmake)
include(${CMAKE_CURRENT_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/hdf5_lib.cmake)

# Set the HDF5 directory to the one conduit used
set(HDF5_DIR ${CONDUIT_HDF5_DIR} CACHE PATH "")

################################
# HDF5
################################
if (HDF5_DIR)
    include(cmake/libraries/FindHDF5.cmake)
    if (HDF5_FOUND)
        blt_register_library( NAME       hdf5
                              TREAT_INCLUDES_AS_SYSTEM ON
                              INCLUDES   ${HDF5_INCLUDE_DIRS}
                              LIBRARIES  ${HDF5_LIBRARIES})
    else()
        message(FATAL_ERROR "Unable to find HDF5 with given path ${HDF5_DIR}")
    endif()
else()
    message(STATUS "Library Disabled: HDF5")
    set(HAVE_HDF5 "0" CACHE STRING "")
endif()


################################
# CONDUIT
################################
if (CONDUIT_DIR)
    include(cmake/libraries/FindConduit.cmake)
    if (CONDUIT_FOUND)
        blt_register_library( NAME       conduit 
                              TREAT_INCLUDES_AS_SYSTEM ON
                              INCLUDES   ${CONDUIT_INCLUDE_DIRS}
                              LIBRARIES  ${CONDUIT_LIBRARIES})
    else()
        message(FATAL_ERROR "Unable to find CONDUIT with given path ${CONDUIT_DIR}")
    endif()
else()
    message(STATUS "Library Disabled: CONDUIT")
    set(HAVE_CONDUIT "0" CACHE STRING "")
endif()
