# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

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

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1

# Include any dependencies generated for this target.
include client/CMakeFiles/mosquitto_pub.dir/depend.make

# Include the progress variables for this target.
include client/CMakeFiles/mosquitto_pub.dir/progress.make

# Include the compile flags for this target's objects.
include client/CMakeFiles/mosquitto_pub.dir/flags.make

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o: client/CMakeFiles/mosquitto_pub.dir/flags.make
client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o: client/pub_client.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/mosquitto_pub.dir/pub_client.c.o   -c /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_client.c

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mosquitto_pub.dir/pub_client.c.i"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_client.c > CMakeFiles/mosquitto_pub.dir/pub_client.c.i

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mosquitto_pub.dir/pub_client.c.s"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_client.c -o CMakeFiles/mosquitto_pub.dir/pub_client.c.s

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.requires:
.PHONY : client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.requires

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.provides: client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.requires
	$(MAKE) -f client/CMakeFiles/mosquitto_pub.dir/build.make client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.provides.build
.PHONY : client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.provides

client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.provides.build: client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o: client/CMakeFiles/mosquitto_pub.dir/flags.make
client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o: client/pub_shared.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/mosquitto_pub.dir/pub_shared.c.o   -c /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_shared.c

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mosquitto_pub.dir/pub_shared.c.i"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_shared.c > CMakeFiles/mosquitto_pub.dir/pub_shared.c.i

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mosquitto_pub.dir/pub_shared.c.s"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/pub_shared.c -o CMakeFiles/mosquitto_pub.dir/pub_shared.c.s

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.requires:
.PHONY : client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.requires

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.provides: client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.requires
	$(MAKE) -f client/CMakeFiles/mosquitto_pub.dir/build.make client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.provides.build
.PHONY : client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.provides

client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.provides.build: client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o: client/CMakeFiles/mosquitto_pub.dir/flags.make
client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o: client/client_shared.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/mosquitto_pub.dir/client_shared.c.o   -c /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_shared.c

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mosquitto_pub.dir/client_shared.c.i"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_shared.c > CMakeFiles/mosquitto_pub.dir/client_shared.c.i

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mosquitto_pub.dir/client_shared.c.s"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_shared.c -o CMakeFiles/mosquitto_pub.dir/client_shared.c.s

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.requires:
.PHONY : client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.requires

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.provides: client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.requires
	$(MAKE) -f client/CMakeFiles/mosquitto_pub.dir/build.make client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.provides.build
.PHONY : client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.provides

client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.provides.build: client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o

client/CMakeFiles/mosquitto_pub.dir/client_props.c.o: client/CMakeFiles/mosquitto_pub.dir/flags.make
client/CMakeFiles/mosquitto_pub.dir/client_props.c.o: client/client_props.c
	$(CMAKE_COMMAND) -E cmake_progress_report /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/CMakeFiles $(CMAKE_PROGRESS_4)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building C object client/CMakeFiles/mosquitto_pub.dir/client_props.c.o"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -o CMakeFiles/mosquitto_pub.dir/client_props.c.o   -c /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_props.c

client/CMakeFiles/mosquitto_pub.dir/client_props.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mosquitto_pub.dir/client_props.c.i"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -E /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_props.c > CMakeFiles/mosquitto_pub.dir/client_props.c.i

client/CMakeFiles/mosquitto_pub.dir/client_props.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mosquitto_pub.dir/client_props.c.s"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && /usr/bin/cc  $(C_DEFINES) $(C_FLAGS) -S /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/client_props.c -o CMakeFiles/mosquitto_pub.dir/client_props.c.s

client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.requires:
.PHONY : client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.requires

client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.provides: client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.requires
	$(MAKE) -f client/CMakeFiles/mosquitto_pub.dir/build.make client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.provides.build
.PHONY : client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.provides

client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.provides.build: client/CMakeFiles/mosquitto_pub.dir/client_props.c.o

# Object files for target mosquitto_pub
mosquitto_pub_OBJECTS = \
"CMakeFiles/mosquitto_pub.dir/pub_client.c.o" \
"CMakeFiles/mosquitto_pub.dir/pub_shared.c.o" \
"CMakeFiles/mosquitto_pub.dir/client_shared.c.o" \
"CMakeFiles/mosquitto_pub.dir/client_props.c.o"

# External object files for target mosquitto_pub
mosquitto_pub_EXTERNAL_OBJECTS =

client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o
client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o
client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o
client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/client_props.c.o
client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/build.make
client/mosquitto_pub: lib/libmosquitto.so.1.5.90
client/mosquitto_pub: /usr/lib64/libssl.so
client/mosquitto_pub: /usr/lib64/libcrypto.so
client/mosquitto_pub: client/CMakeFiles/mosquitto_pub.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking C executable mosquitto_pub"
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mosquitto_pub.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
client/CMakeFiles/mosquitto_pub.dir/build: client/mosquitto_pub
.PHONY : client/CMakeFiles/mosquitto_pub.dir/build

client/CMakeFiles/mosquitto_pub.dir/requires: client/CMakeFiles/mosquitto_pub.dir/pub_client.c.o.requires
client/CMakeFiles/mosquitto_pub.dir/requires: client/CMakeFiles/mosquitto_pub.dir/pub_shared.c.o.requires
client/CMakeFiles/mosquitto_pub.dir/requires: client/CMakeFiles/mosquitto_pub.dir/client_shared.c.o.requires
client/CMakeFiles/mosquitto_pub.dir/requires: client/CMakeFiles/mosquitto_pub.dir/client_props.c.o.requires
.PHONY : client/CMakeFiles/mosquitto_pub.dir/requires

client/CMakeFiles/mosquitto_pub.dir/clean:
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client && $(CMAKE_COMMAND) -P CMakeFiles/mosquitto_pub.dir/cmake_clean.cmake
.PHONY : client/CMakeFiles/mosquitto_pub.dir/clean

client/CMakeFiles/mosquitto_pub.dir/depend:
	cd /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1 /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1 /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client /home/west/Plugfest2019/P21451-1-6/MQTTbroker/mosquitto-mqtt5-test1/client/CMakeFiles/mosquitto_pub.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : client/CMakeFiles/mosquitto_pub.dir/depend

