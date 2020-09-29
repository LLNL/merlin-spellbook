# Copyright (c) 2010, Lawrence Livermore National Security, LLC. Produced at the
# Lawrence Livermore National Laboratory. LLNL-CODE-443211. All Rights reserved.
# See file COPYRIGHT for details.
#
# This file is part of the MFEM library. For more information and source code
# availability see http://mfem.org.
#
# MFEM is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License (as published by the Free
# Software Foundation) version 2.1 dated February 1999.

# Defines the following variables:
#   - CONDUIT_FOUND
#   - CONDUIT_LIBRARIES
#   - CONDUIT_INCLUDE_DIRS


#find includes
find_path( CONDUIT_INCLUDE_DIRS conduit/conduit_relay_hdf5.hpp
           PATHS  ${CONDUIT_DIR}/include/
           NO_DEFAULT_PATH
           NO_CMAKE_ENVIRONMENT_PATH
           NO_CMAKE_PATH
           NO_SYSTEM_ENVIRONMENT_PATH
           NO_CMAKE_SYSTEM_PATH)

set(CONDUIT_NAMES 
    conduit
    conduit_blueprint
    conduit_relay
    conduit_relay_mpi
    )

blt_find_libraries(FOUND_LIBS CONDUIT_LIBRARIES
                   NAMES ${CONDUIT_NAMES}
                   PATHS ${CONDUIT_DIR}/lib
                   )

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set CONDUIT_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(CONDUIT  DEFAULT_MSG
                                  CONDUIT_INCLUDE_DIRS
                                  CONDUIT_LIBRARIES )
