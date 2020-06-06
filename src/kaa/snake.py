import setuptools
import os

def rattle():
	return setuptools.setup(
		entry_points={
	        "console_scripts": [
	            "kaa = kaa.main:rattle"
	        ],
		}


	)

rattle()
