#!/bin/bash

# create & activate new conda env: streamlit environment
conda create -n stenv python=3.11
conda activate stenv

# install streamlit
pip install streamlit -y

# launch streamlit demo
streamlit hello