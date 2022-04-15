from setuptools import setup, find_packages

setup(
    name='piaware_exporter',
    version="1.0",
    description="Prometheus exporter for PiAware",
    url="",
    author="Eric Tran",
    author_email="eric1tran@gmail.com",
    license="MIT",
    packages=["piaware_exporter"],
    install_requires=[
        "prometheus-client",
        "requests"
    ]
)
