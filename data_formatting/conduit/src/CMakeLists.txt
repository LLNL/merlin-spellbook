
set(GATHER_SRC conduit_gather.cpp)

blt_add_executable(NAME conduit_gather
                   SOURCES ${GATHER_SRC}
                   DEPENDS_ON conduit)
