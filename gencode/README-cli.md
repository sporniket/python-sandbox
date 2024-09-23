# $$$Whatever CLI

**Content**

1. User manual
2. $$$Other things noteworthy...

## User Manual

### Synopsys

`$$$whatever [--help] [<source files>...]`

#### Positional arguments

* `<source files>...` : an optionnal list of source files ; when no files are provided, use the standard input instead.

#### Options

*  `-h`, `--help`: shows an help message and exits.
*  $$$...

### Description

Reads the standard input or a list of input files, and $$$do whatever

### Typical invocation

**Given** an input file `mysource.s`

#### Using redirection

```
$$$whatever <mysource.s >somewhere.s
```

#### Using pipe

```
cat mysource.s | $$$whatever | cat > somewhere.s
```

#### Batch processing all the source files of the current folder

> _Written for the bash shell_

* Each source file is unconditionnaly rewritten :

```
for fic in $(ls *.s); do mv $fic tmp.$fic ; $$$whatever <tmp.$fic >$fic ; rm tmp.$fic ; done
```

## $$$Other things noteworthy...

whatever...