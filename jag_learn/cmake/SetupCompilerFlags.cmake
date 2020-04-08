

set(MERLIN_PROMOTE_WARNINGS FALSE CACHE BOOL "")
set(BLT_CXX_STD "c++11" CACHE BOOL "")

#
# Should not have to do this but cmake doesnt support enabling 
# intel compilers for c++11
#
if (${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION} LESS 3.8)
    if (COMPILER_FAMILY_IS_INTEL AND BLT_CXX_STD STREQUAL "c++11")
        set(CXX_SRC_FLAGS "${CXX_SRC_FLAGS} -std=c++11")
    endif()
endif()

#######################################################################
#                              C++ Flags
#######################################################################

# enable the 'restrict' keyword for disambiguating pointers
blt_append_custom_compiler_flag(
    FLAGS_VAR restrict_flag
    DEFAULT  " "
    CLANG    " "
    GNU      " "
    INTEL    "-restrict"
    XL       " "
    )
set(CXX_SRC_FLAGS "${CXX_SRC_FLAGS} ${restrict_flag}")

# Warning flags
# Add the -Wno-missing-braces to get around the clang
#  bug https://llvm.org/bugs/show_bug.cgi?id=21629. 10/24/2016
blt_append_custom_compiler_flag(
    FLAGS_VAR CXX_SRC_FLAGS_DEBUG
    DEFAULT  " "
    CLANG    "-Wno-type-safety -Wno-self-assign -Wno-unknown-pragmas -Wno-missing-braces"
    GNU      "-Wunused-variable -Wsign-compare"
    INTEL    "-wd2282 -Wall -Wcheck -wd193 -wd279 -wd383 -wd981 -wd1572 -wd161 -wd3346 -Wunused-variable -Wremarks"
    XL       " "
    )

if (MERLIN_PROMOTE_WARNINGS)
   blt_append_custom_compiler_flag(
       FLAGS_VAR CXX_SRC_FLAGS_DEBUG
       DEFAULT  "-Werror"
       INTEL    "-Werror-all"
       )
endif()

#######################################################################
#                              C Flags
#######################################################################

set(C_SRC_FLAGS "${C_SRC_FLAGS} ${restrict_flag}")

# Warning flags
blt_append_custom_compiler_flag(
    FLAGS_VAR C_SRC_FLAGS_DEBUG
    DEFAULT  " "
    CLANG    "-Wno-type-safety -Wno-self-assign -Wno-unknown-pragmas"
    GNU      "-Wsign-compare"
    INTEL    "-wd2282 -Wall -Wcheck -wd193 -wd279 -wd383 -wd981 -wd1572 -wd161 -wd3346"
    XL       " "
    )

if (MERLIN_PROMOTE_WARNINGS)
   blt_append_custom_compiler_flag(
       FLAGS_VAR C_SRC_FLAGS_DEBUG
       DEFAULT  "-Werror"
       INTEL    "-Werror-all"
       )
endif()

#######################################################################
#                           CUDA Flags
#######################################################################

# Set optimization level
# Note: multi-config generators do not seem to be supported yet for CUDA
if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    list (APPEND CUDA_NVCC_FLAGS -G -O0 -g -Xcompiler '-g' -Xcompiler '-O0' --expt-relaxed-constexpr)
else()
    list (APPEND CUDA_NVCC_FLAGS -O3 -Xcompiler '-O3' -lineinfo --expt-relaxed-constexpr)
endif()

#######################################################################
#                           Fortran Flags
#######################################################################

# Warning flags
blt_append_custom_compiler_flag(
    FLAGS_VAR Fortran_SRC_FLAGS_DEBUG
    DEFAULT  " "
    )

if (MERLIN_PROMOTE_WARNINGS)
   blt_append_custom_compiler_flag(
       FLAGS_VAR Fortran_SRC_FLAGS_DEBUG
       DEFAULT  "-Werror"
       INTEL    "-warn error"
       )
endif()

#######################################################################
#                           Linker Flags
#######################################################################

# enable export of symbols for dynamic linking
if (VISIT_FOUND)
    blt_append_custom_compiler_flag(
        FLAGS_VAR export_dynamic
        DEFAULT  " "
        CLANG    " "
        GNU      " "
        INTEL    " "
        XL       " "
        )
endif()

# Set the compiler flags with the SRC-only flags.
foreach(_LANG C CXX Fortran)
   set(CMAKE_${_LANG}_FLAGS "${CMAKE_${_LANG}_FLAGS} ${${_LANG}_SRC_FLAGS}")
   foreach(_BUILDTYPE DEBUG RELEASE RELWITHDEBINFO MINSIZEREL)
      set(CMAKE_${_LANG}_FLAGS_${_BUILDTYPE} "${CMAKE_${_LANG}_FLAGS_${_BUILDTYPE}} ${${_LANG}_SRC_FLAGS_${_BUILDTYPE}}")
   endforeach()
endforeach()
