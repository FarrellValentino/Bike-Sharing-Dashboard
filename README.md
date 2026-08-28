# Bike Sharing Data Dashboard 🚲

Dashboard interaktif ini dibuat untuk menganalisis data penyewaan sepeda (Bike Sharing Dataset) berdasarkan faktor lingkungan, musim, dan waktu operasional. 

Link dashboard: https://bike-sharing-dashboard-tokbnnmgaxcqjb47f9w4bq.streamlit.app/

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/ Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
py -m streamlit run dashboard/app.py 
```