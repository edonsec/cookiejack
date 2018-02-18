from setuptools import setup, find_packages

setup(
    name="cookiejack",
    version="0.0.1a",
    description="Sniff cookies off the wire and send them via a websocket.",
    author="Ed Cradock",
    license="MIT",
    packages=find_packages(),
    install_requires=["autobahn", "Twisted", "requests", "scapy", "chardet", "tld", "zope.interface", "attrs"],
    entry_points={
        "console_scripts": [
            "cookiejack=cookiejack:main"
        ]
    }
)
