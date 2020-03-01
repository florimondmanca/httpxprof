# httpxprof

A tool for profiling [HTTPX](https://github.com/encode/httpx) using cProfile and [SnakeViz](https://jiffyclub.github.io/snakeviz/).

![](assets/example.png)

## Installation

- Install the version of HTTPX you'd like to profile against.
- Install this tool using pip:

```bash
pip install -e git+https://github.com/florimondmanca/httpxprof#egg=httpxprof
```

## Usage

```bash
# Run one of the built-in profiling cases:
httpxprof run async_client

# View results:
httpxprof view async_client

# You can also run your profiling cases by passing Python scripts:
httpxprof run path/to/my_case.py
httpxprof view path/to/my_case.py
```

You can ask for `--help` on `httpxprof` and any of the subcommands.
