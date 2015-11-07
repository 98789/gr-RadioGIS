INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RADIOGIS RadioGIS)

FIND_PATH(
    RADIOGIS_INCLUDE_DIRS
    NAMES RadioGIS/api.h
    HINTS $ENV{RADIOGIS_DIR}/include
        ${PC_RADIOGIS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RADIOGIS_LIBRARIES
    NAMES gnuradio-RadioGIS
    HINTS $ENV{RADIOGIS_DIR}/lib
        ${PC_RADIOGIS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RADIOGIS DEFAULT_MSG RADIOGIS_LIBRARIES RADIOGIS_INCLUDE_DIRS)
MARK_AS_ADVANCED(RADIOGIS_LIBRARIES RADIOGIS_INCLUDE_DIRS)

