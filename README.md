
# PrivGuard

This repository is a modified version of PrivGuard. PrivGuard is a a proof-of-concept implementation of [PrivAnalyzer](https://wanglun1996.github.io/publication/poly19.pdf).

Original PrivGuard repository: https://github.com/sunblaze-ucb/privguard-artifact

## Prerequisite

The static analyzer has been tested in MacOS Sonoma 14.3.1 using a `conda` virtual environment. Personally, I chose to install Anaconda by following the official installation instructions provided by Anaconda.
You can download the installer for your OS from the Anaconda [website](https://www.anaconda.com/download) and follow the installation instructions.

Miniconda should work as well.

Once Anaconda or Miniconda is installed, you can create a new conda virtual environment tailored for this repository by running:

```
conda create -n thenameyoupreferforthisrepo
conda activate name
```

If you have an Apple Silicon device, you will have to emulate the x86 architecture by executing these two additional lines before proceeding with the next steps:

```
softwareupdate --install-rosetta
conda config --env --set subdir osx-64
```

Please, make sure to install python 3.6 as your python version by executing:

```
conda install python=3.6
```

Now, download the source code of the static analyzer:

```
git clone https://github.com/filvan/privGuard.git
```

Finally, enter the root directory of the repo and activate your previously created virtual environment. Install the required packages and set environment variables by running:

```
chmod u+x ./setup.sh
./setup.sh
```

## How to use

This codebase contains (1) a policy parser to translate Legalease policy strings into Python object; (2) a set of function summaries specifying the privacy effect of commonly used data analysis functions; (3) a static analyzer that checks whether a Python program satisfies a Legalease policy.

To test the policy parser, run:

```
python path-to-repo/src/parser/policy_parser.py
```

and input a valid policy string (e.g. "ALLOW FILTER age >= 18 AND SCHEMA NotPHI, h2 AND FILTER gender == 'M' ALLOW (FILTER gender == 'M' OR (FILTER gender == 'F' AND SCHEMA PHI))") in Legalease. The program will output the policy translated to Python objects.

To test converting a policy into its DNF form, run:

```
python path-to-repo/src/parser/policy_tree.py
```

## Code structure

The code is organized into three sub-directories under `src` directory: (1) `parser` which contains the parser and implementation of PrivGuard policies; (2) `stub_libraries` which contains the implementation of function summaries; (3) `examples` which contains the example programs and corresponding policies.

The organization of the `parser directory` is as below:

```
            policy_tree.py
                 |
           policy_parser.py
           /           \
abstract_domain.py     attribute.py
      |
typed_value.py
```

typed_value.py defines the basic values types (e.g. integers, strings) used in the policy. abstract_domain.py defines the corresponding lattice built on top of the defined values. attribute.py defines the attributes in the policy. policy_parser.py is the real parser that converts the policy strings into lists of basic tokens. policy_tree.py further organizes the tokens in a tree structure convenient for analysis.

## Example Test Cases

This version comes together with three benchmark open-source programs that can be tested for privacy compliance.
These programs are: LibreTaxi, Selfmailbot and Traccar.
The codebases of these software have been entirely translated in Python (whenever necessary) to make theme understandable by PrivAnalyzer. The so-generated source code Python files have been grouped in folders, that can be found in the [program](./src/examples/program/) directory.
These files can then be used as example test cases for the static analyzer in the way I am gonna explain now.

First, make sure to choose the correct filepath for both your policy and your meta data specification files inside the [stub_pandas.py](./src/stub_libraries/stub_pandas.py) file. Indeed, the analyzer will use these files as sources to get the rules to enforce and the conceptual schema.

Second, choose a source code file to analyze and look for the corresponding `example_id` in the `program_map` dictionary, inside the [analyze.py](./src/analyze.py) file.

Now you can run a command like this from your terminal:

```
python path-to-repo/src/analyze.py --example_id theexampleidyouchose
```
