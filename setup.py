from setuptools import find_packages, setup

setup(
    name="httpxprof",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "click==7.*",
        "snakeviz==2.*",
        "uvicorn==0.11.*",
        "tqdm==4.*",
        "trustme==0.6.*",
    ],
    entry_points="""
        [console_scripts]
        httpxprof=httpxprof.main:cli
    """,
)
