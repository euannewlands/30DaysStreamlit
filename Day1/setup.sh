#!/bin/bash

# create & activate new conda env: streamlit environment
conda create -n stenv python=3.11 -y
conda.bat activate stenv

# install streamlit,with auto yes to install/update packages
yes | pip install streamlit

# launch streamlit demo
streamlit hello