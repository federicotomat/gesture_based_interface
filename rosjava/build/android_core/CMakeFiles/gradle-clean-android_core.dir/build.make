# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

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
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/federico/rosjava/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/federico/rosjava/build

# Utility rule file for gradle-clean-android_core.

# Include the progress variables for this target.
include android_core/CMakeFiles/gradle-clean-android_core.dir/progress.make

android_core/CMakeFiles/gradle-clean-android_core:
	cd /home/federico/rosjava/src/android_core && /home/federico/rosjava/build/catkin_generated/env_cached.sh /home/federico/rosjava/src/android_core/gradlew clean

gradle-clean-android_core: android_core/CMakeFiles/gradle-clean-android_core
gradle-clean-android_core: android_core/CMakeFiles/gradle-clean-android_core.dir/build.make

.PHONY : gradle-clean-android_core

# Rule to build all files generated by this target.
android_core/CMakeFiles/gradle-clean-android_core.dir/build: gradle-clean-android_core

.PHONY : android_core/CMakeFiles/gradle-clean-android_core.dir/build

android_core/CMakeFiles/gradle-clean-android_core.dir/clean:
	cd /home/federico/rosjava/build/android_core && $(CMAKE_COMMAND) -P CMakeFiles/gradle-clean-android_core.dir/cmake_clean.cmake
.PHONY : android_core/CMakeFiles/gradle-clean-android_core.dir/clean

android_core/CMakeFiles/gradle-clean-android_core.dir/depend:
	cd /home/federico/rosjava/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/federico/rosjava/src /home/federico/rosjava/src/android_core /home/federico/rosjava/build /home/federico/rosjava/build/android_core /home/federico/rosjava/build/android_core/CMakeFiles/gradle-clean-android_core.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : android_core/CMakeFiles/gradle-clean-android_core.dir/depend

