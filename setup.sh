#!/bin/bash
echo "Inicializando configuración en Streamlit..."
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install plotly pandas streamlit matplotlib
