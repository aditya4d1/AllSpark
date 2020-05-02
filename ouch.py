"""
AllSpark: C/C++/CUDA project generator

This file generates projects for
1. C
2. C++
3. CUDA

The contents of these generated projects are: 

.clang-format
Makefile
directory structure
README
LICENSE
.ci.yml

Possible arguments to the file

--lang = c, cpp, cu
--license = mit, apache
--author = <author name>
--email = <author email>
--name = <project name>
--desc = <project description>
"""

import argparse
import os
import datetime
import sources
from license import licenses

parser = argparse.ArgumentParser(description="TODO!")
parser.add_argument("--lang", action="store", required=True, type=str, choices=["c", "cpp", "cu"], help="TODO!")
parser.add_argument("--compiler", action="store", required=False, type=str, default="gnu", choices=["gnu", "clang"], help="TODO!")
parser.add_argument("--license", action="store", required=True, type=str, choices=["mit", "apache"], help="TODO!")
parser.add_argument("--author", action="store", required=True, type=str, help="TODO!")
parser.add_argument("--email", action="store", required=True, type=str, help="TODO!")
parser.add_argument("--name", action="store", required=True, type=str, help="TODO!")
parser.add_argument("--desc", action="store", required=True, type=str, help="TODO!")
parser.add_argument("--parent-dir", action="store", required=False, type=str, help="TODO!")
args = parser.parse_args()

def generate_directory_structure_c_deriv(parent_dir, project_name, req_lic, author, email, desc, lang, cc):
  """Create project and populate it with contents"""
  ## Create required directories
  cwd = os.getcwd() + "/../" + project_name
  os.makedirs(cwd, exist_ok=True)
  cwd_include = cwd + "/include"
  os.makedirs(cwd_include, exist_ok=True)
  cwd_include_project = cwd_include + "/" + project_name
  os.makedirs(cwd_include_project, exist_ok=True)
  cwd_src = cwd + "/src"
  os.makedirs(cwd_src, exist_ok=True)
  cwd_src_include = cwd_src + "/include"
  os.makedirs(cwd_src_include, exist_ok=True)
  cwd_tests = cwd + "/tests"
  os.makedirs(cwd_tests, exist_ok=True)

  ## Create license file
  f = open(cwd + "/LICENSE", "w")
  year = datetime.datetime.now().strftime("%Y")
  lic = licenses[req_lic + "_pre"]  + "%s %s <%s>" % (year, author, email) + licenses[req_lic + "_post"]
  f.write(lic)
  f.close()

  ## Create README file
  f = open(cwd + "/README.md", "w")
  f.write("# README\n%s\n" % desc)
  f.close()

  ## Create .clang-format file
  f = open(cwd + "/.clang-format", "w")
  f.write(sources.clang_format)
  f.close()

  ## Create Makefile
  # open Makefile
  f = open(cwd_src + "/Makefile", "w")
  if lang == "c":
    f.write("CC=%s\n" % "gcc" if cc == "gnu" else "clang")
    f.write("CCFLAGS=-I../include -I./include")
  if lang == "cpp" or lang == "cu":
    f.write("CC=%s\nCXX=%s\n" % ("gcc", "g++") if cc == "gnu" else ("clang", "clang++"))
    f.write("CCFLAGS=-I../include -I./include\n")
    f.write("CXXFLAGS=-I../include -I./include -std=c++14\n")
  if lang == "cu":
    f.write("NVCC=nvcc\n")
  
  if lang == "c":
    f.write("""\n
all: %s

%s: %s.c
\tmkdir -p bin
\t$(CC) $(CCFLAGS) $^ -o ./bin/$@
clean:
\trm -rf bin
  """ % (project_name, project_name, project_name))
  elif lang == "cpp":
    f.write("""\n
all: %s

%s: %s.cpp
\tmkdir -p bin
\t$(CXX) $(CXXFLAGS) $^ -o ./bin/$@
clean:
\trm -rf bin
  """ % (project_name, project_name, project_name))
  elif lang == "cu":
    f.write("""\n
all: %s

%s: %s.cu
\tmkdir -p bin
\t$(NVCC) $(CXXFLAGS) $^ -o ./bin/$@
clean:
\trm -rf bin
  """ % (project_name, project_name, project_name))
  f.close()
  # close Makefile

  preamble_final = sources.preamble % (year, author, email)
  project_name_upper = project_name.upper()
  project_name_upper = project_name_upper.replace("-", "_")

  ## Create project_name.h in ./include/project_name
  # open ./include/project_name/project_name.h
  f = open(cwd_include_project + "/" + project_name + ".h", "w")
  f.write(preamble_final + sources.hdr_inc % (project_name_upper, project_name_upper, project_name_upper, project_name_upper, project_name_upper, project_name_upper))
  f.close()
  # close ./include/project_name/project_name.h

  ## Create project_name.h in ./src/include
  # open ./src/include/project_name.h
  f = open(cwd_src_include + "/" + project_name + ".h", "w")
  f.write(preamble_final + sources.hdr_src_inc % (project_name_upper, project_name_upper, project_name_upper, project_name_upper))
  f.close()
  # close ./src/include/project_name.h

  ## Create defines.h for CUDA in ./src/include
  if lang == "cu":
    f = open(cwd_src_include + "/defines.h", "w")
    f.write(preamble_final + sources.cu_hdr_src_inc % (project_name_upper, project_name_upper))
    f.close()

  ## Create project_name.lang in ./src
  if lang == "c":
    f = open(cwd_src + "/" + project_name + ".c", "w")
    f.write(preamble_final + sources.cc_src % (project_name, project_name, project_name, project_name))
    f.close()
  if lang == "cpp":
    f = open(cwd_src + "/" + project_name + ".cpp", "w")
    f.write(preamble_final + sources.cxx_src % (project_name, project_name, project_name, project_name))
    f.close()
  if lang == "cu":
    f = open(cwd_src + "/" + project_name + ".cu", "w")
    f.write(preamble_final + sources.cu_src % (project_name, project_name, project_name, project_name, project_name))
    f.close()

  ## Create github workflows (CI files)
  cwd_workflows = cwd + "/.github/workflows"
  os.makedirs(cwd_workflows, exist_ok=True)
  f = open(cwd_workflows + "/ci.yml", "w")
  f.write(sources.ci % (project_name, project_name))
  f.close()

  

if __name__ == "__main__":
  print(args.lang)
  print(args.license)
  print(args.author)
  print(args.email)
  print(args.name)
  print(args.desc)
  generate_directory_structure_c_deriv("", args.name, args.license, args.author, args.email, args.desc, args.lang, args.compiler)
