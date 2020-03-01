from setuptools import find_packages, setup

setup(
    name="httpxprof",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["click", "httpx", "snakeviz", "uvicorn", "tqdm"],
    entry_points="""
        [console_scripts]
        httpxprof=httpxprof.main:cli
    """,
)
