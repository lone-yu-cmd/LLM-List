from setuptools import setup, find_packages

setup(
    name="llm-list",
    version="1.0.0",
    description="Standardized LLM registry data",
    author="LLMList Contributors",
    packages=find_packages(),
    package_data={
        "llm_list": ["data/llm_registry.json"],
    },
    include_package_data=True,
    python_requires=">=3.8",
)
