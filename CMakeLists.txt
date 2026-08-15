cmake_minimum_required(VERSION 3.15...4.3)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(
  Python
  COMPONENTS Interpreter Development.Module
  REQUIRED)

python_add_library(_laziness MODULE src/laziness/_laziness.c WITH_SOABI)
install(TARGETS _laziness DESTINATION .)
