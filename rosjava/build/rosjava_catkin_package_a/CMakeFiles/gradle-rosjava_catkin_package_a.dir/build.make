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

# Utility rule file for gradle-rosjava_catkin_package_a.

# Include the progress variables for this target.
include rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/progress.make

rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/federico/rosjava/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Gradling tasks for rosjava_catkin_package_a"
	cd /home/federico/rosjava/src/rosjava_catkin_package_a && ROS_MAVEN_REPOSITORY=https://github.com/rosjava/rosjava_mvn_repo/raw/master /home/federico/rosjava/build/catkin_generated/env_cached.sh /home/federico/rosjava/src/rosjava_catkin_package_a/gradlew -q installDist publish

gradle-rosjava_catkin_package_a: rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a
gradle-rosjava_catkin_package_a: rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/build.make

.PHONY : gradle-rosjava_catkin_package_a

# Rule to build all files generated by this target.
rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/build: gradle-rosjava_catkin_package_a

.PHONY : rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/build

rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/clean:
	cd /home/federico/rosjava/build/rosjava_catkin_package_a && $(CMAKE_COMMAND) -P CMakeFiles/gradle-rosjava_catkin_package_a.dir/cmake_clean.cmake
.PHONY : rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/clean

rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/depend:
	cd /home/federico/rosjava/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/federico/rosjava/src /home/federico/rosjava/src/rosjava_catkin_package_a /home/federico/rosjava/build /home/federico/rosjava/build/rosjava_catkin_package_a /home/federico/rosjava/build/rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : rosjava_catkin_package_a/CMakeFiles/gradle-rosjava_catkin_package_a.dir/depend

