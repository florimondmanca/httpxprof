from setuptools import setup

setup(
    name="httpxprof",
    version="0.1",
    py_modules=["main"],
    install_requires=["click", "httpx", "snakeviz", "uvicorn"],
    entry_points="""
        [console_scripts]
        httpxprof=main:cli
    """,
)
