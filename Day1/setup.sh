#!/bin/bash

# create & activate new conda env: streamlit environment
conda create -n stenv python=3.11 -y
source activate base
conda activate stenv

# install streamlit,with auto yes to install/update packages
yes | pip install streamlit

# launch streamlit demo
streamlit hello