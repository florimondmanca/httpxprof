**NOTICE**: This project was integrated into [HTTPX](https://github.com/encode/httpx) and is now unmaintained.

---

# httpx-profile

A tool for profiling [HTTPX](https://github.com/encode/httpx) using cProfile and [SnakeViz](https://jiffyclub.github.io/snakeviz/).

## Usage

```bash
# Start the supporting server
httpxprof serve

# Run a benchmark (see httpxprof run --help for available options).
httpxprof run async

# View benchmark results
httpxprof view async
```

## Installation

```bash
python -m venv venv
. venv/bin/activate
pip install -e .
```
