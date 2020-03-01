# httpxprof

A tool for profiling [HTTPX](https://github.com/encode/httpx) using cProfile and [SnakeViz](https://jiffyclub.github.io/snakeviz/).

![](assets/example.png)

## Installation

- Install the version of HTTPX you'd like to profile against.
- Install this tool using pip:

```bash
pip install git+https://github.com/florimondmanca/httpxprof
```

## Usage

```bash
# Run one of the profiling cases:
httpxprof run async

# View results:
httpxprof view async
```

You can ask for `--help` on `httpxprof` and any of the subcommands.
