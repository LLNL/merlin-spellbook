
# first Check for HDF5_DIR

if(NOT HDF5_DIR)
    MESSAGE(FATAL_ERROR "Could not find HDF5. HDF5 support needs explicit HDF5_DIR")
endif()

#find includes
find_path( HDF5_INCLUDE_DIRS hdf5.h
           PATHS  ${HDF5_DIR}/include/
           NO_DEFAULT_PATH
           NO_CMAKE_ENVIRONMENT_PATH
           NO_CMAKE_PATH
           NO_SYSTEM_ENVIRONMENT_PATH
           NO_CMAKE_SYSTEM_PATH)

set(HDF5_NAMES
    hdf5
    hdf5_hl
    )

blt_find_libraries(FOUND_LIBS HDF5_LIBRARIES
                   NAMES ${HDF5_NAMES}
                   PATHS ${HDF5_DIR}/lib
                   )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set HDF5_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(HDF5  DEFAULT_MSG
                                  HDF5_INCLUDE_DIRS
                                  HDF5_LIBRARIES )
