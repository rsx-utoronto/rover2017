# Lidar software

## Dependencies

- octomap: Octomap is a C++ library (with python bindings) that uses lidar data to create a 3D occupancy map. To install, first follow the installation instructions on the octomap github here then follow the installation instructions on for the python bindings here. Make sure that you download octomap version 1.7.2, **not** the current version, version 1.8. This is because the person who made the python bindings does not seem to thave updated them since octomap version 1.8 was released. To find octomap version 1.7.2, look under the "Releases" tab on the github page. If after successfully installing everything you encounter an error similar to "couldn't find libxxxxxx.so.1.7" while trying to run a file containing "import octomap", make sure that you have /usr/local/lib in your environment variable LD_LIBRARY_PATH (see stackoverflow here).
