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


# Produce verbose output by default.
VERBOSE = 1

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
CMAKE_SOURCE_DIR = /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp

# Include any dependencies generated for this target.
include CMakeFiles/cmTC_d3433.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cmTC_d3433.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cmTC_d3433.dir/flags.make

CMakeFiles/cmTC_d3433.dir/src.c.o: CMakeFiles/cmTC_d3433.dir/flags.make
CMakeFiles/cmTC_d3433.dir/src.c.o: src.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/cmTC_d3433.dir/src.c.o"
	/Users/Clemsut/emsdk/emscripten/1.37.36/emcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/cmTC_d3433.dir/src.c.o   -c /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/src.c

CMakeFiles/cmTC_d3433.dir/src.c.i: cmake_force
	@echo "Preprocessing C source to CMakeFiles/cmTC_d3433.dir/src.c.i"
	/Users/Clemsut/emsdk/emscripten/1.37.36/emcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/src.c > CMakeFiles/cmTC_d3433.dir/src.c.i

CMakeFiles/cmTC_d3433.dir/src.c.s: cmake_force
	@echo "Compiling C source to assembly CMakeFiles/cmTC_d3433.dir/src.c.s"
	/Users/Clemsut/emsdk/emscripten/1.37.36/emcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/src.c -o CMakeFiles/cmTC_d3433.dir/src.c.s

# Object files for target cmTC_d3433
cmTC_d3433_OBJECTS = \
"CMakeFiles/cmTC_d3433.dir/src.c.o"

# External object files for target cmTC_d3433
cmTC_d3433_EXTERNAL_OBJECTS =

cmTC_d3433.js: CMakeFiles/cmTC_d3433.dir/src.c.o
cmTC_d3433.js: CMakeFiles/cmTC_d3433.dir/build.make
cmTC_d3433.js: CMakeFiles/cmTC_d3433.dir/objects1.rsp
cmTC_d3433.js: CMakeFiles/cmTC_d3433.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable cmTC_d3433.js"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cmTC_d3433.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cmTC_d3433.dir/build: cmTC_d3433.js

.PHONY : CMakeFiles/cmTC_d3433.dir/build

CMakeFiles/cmTC_d3433.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cmTC_d3433.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cmTC_d3433.dir/clean

CMakeFiles/cmTC_d3433.dir/depend:
	cd /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp /Users/Clemsut/Desktop/facerec/opencv/CMakeFiles/CMakeTmp/CMakeFiles/cmTC_d3433.dir/DependInfo.cmake
.PHONY : CMakeFiles/cmTC_d3433.dir/depend

