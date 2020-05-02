"""
Contains sources for different files
"""

preamble = """\
/**
 * This file is covered by the LICENSE file in the root of this project.
 * Copyright %s %s <%s>
 */
"""

hdr_inc = """\
#pragma once

#ifndef %s_INCLUDE_%s_%s_H
#define %s_INCLUDE_%s_%s_H

/**
* All external header declarations go here!
*/

#endif
"""

hdr_src_inc = """\
#pragma once

#ifndef %s_SRC_INCLUDE_%s_H
#define %s_SRC_INCLUDE_%s_H

/**
* All internal header declarations go here!
*/

#endif
"""

cu_hdr_src_inc = """\
#pragma once

#ifndef %s_SRC_INCLUDE_DEFINES_H
#define %s_SRC_INCLUDE_DEFINES_H

#define CUDA_CHECK(status) \\
  { \\
    cudaError_t err = status; \\
    std::cerr << __FILE__ << ":" << __LINE__ << ": " << cudaGetErrorString(err) << std::endl; \\
    return 0; \\
  } \\
#endif
"""

cc_src = """\

#include <stdio.h>

#include "%s.h"
#include "%s/%s.h"

int main(int argc, char *argv[]) {
  printf("Welcome to project: %s\\n");
  return 0;
}

"""

cxx_src = """\

#include <iostream>

#include "%s.h"
#include "%s/%s.h"

int main(int argc, char *argv[]) {
  std::cout << "Welcome to project: %s\\n" << std::endl;
  return 0;
}

"""

cu_src = """\

#include <iostream>

#include <cuda.h>
#include "cuda_runtime.h"

#include "%s.h"
#include "%s/%s.h"
#include "%s/defines.h"


int main(int argc, char *argv[]) {
  std::cout << "Welcome to CUDA project: %s\\n" << std::endl;
  return 0;
}

"""


clang_format = """\
BasedOnStyle: Google
AccessModifierOffset: -2
IndentCaseLabels: false
PointerBindsToType: false
Standard: Cpp11
IndentWidth: 2
"""

ci = """\
name: %s

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: %s
      run: cd src; make
"""