# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_fs_robot_description_jazzy_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED fs_robot_description_jazzy_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(fs_robot_description_jazzy_FOUND FALSE)
  elseif(NOT fs_robot_description_jazzy_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(fs_robot_description_jazzy_FOUND FALSE)
  endif()
  return()
endif()
set(_fs_robot_description_jazzy_CONFIG_INCLUDED TRUE)

# output package information
if(NOT fs_robot_description_jazzy_FIND_QUIETLY)
  message(STATUS "Found fs_robot_description_jazzy: 0.0.1 (${fs_robot_description_jazzy_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'fs_robot_description_jazzy' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT fs_robot_description_jazzy_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(fs_robot_description_jazzy_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${fs_robot_description_jazzy_DIR}/${_extra}")
endforeach()
