# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.11

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.11.0/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.11.0/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/Clemsut/opencv

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/Clemsut/Desktop/facerec/opencv/build_wasm

# Utility rule file for gen-pkgconfig.

# Include the progress variables for this target.
include CMakeFiles/gen-pkgconfig.dir/progress.make

unix-install/opencv.pc: OpenCVGenPkgConfig.info.cmake
unix-install/opencv.pc: /Users/Clemsut/opencv/cmake/OpenCVGenPkgconfig.cmake
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/Clemsut/Desktop/facerec/opencv/build_wasm/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generate opencv.pc"
	/usr/local/Cellar/cmake/3.11.0/bin/cmake -DCMAKE_HELPER_SCRIPT=/Users/Clemsut/Desktop/facerec/opencv/build_wasm/OpenCVGenPkgConfig.info.cmake -P /Users/Clemsut/opencv/cmake/OpenCVGenPkgconfig.cmake

gen-pkgconfig: unix-install/opencv.pc
gen-pkgconfig: CMakeFiles/gen-pkgconfig.dir/build.make

.PHONY : gen-pkgconfig

# Rule to build all files generated by this target.
CMakeFiles/gen-pkgconfig.dir/build: gen-pkgconfig

.PHONY : CMakeFiles/gen-pkgconfig.dir/build

CMakeFiles/gen-pkgconfig.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/gen-pkgconfig.dir/cmake_clean.cmake
.PHONY : CMakeFiles/gen-pkgconfig.dir/clean

CMakeFiles/gen-pkgconfig.dir/depend:
	cd /Users/Clemsut/Desktop/facerec/opencv/build_wasm && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/Clemsut/opencv /Users/Clemsut/opencv /Users/Clemsut/Desktop/facerec/opencv/build_wasm /Users/Clemsut/Desktop/facerec/opencv/build_wasm /Users/Clemsut/Desktop/facerec/opencv/build_wasm/CMakeFiles/gen-pkgconfig.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/gen-pkgconfig.dir/depend

