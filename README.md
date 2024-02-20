# CODERHOUSE DE Pre Entrega 2

>Ariel Calzada 

>ariel.calzada@gmail.com

## Objetivos

- Generar ETLs a partir de información de APIs usando las librerías requests, 
  json, psycopg2/SqlAlchemy y pandas

- Solucionar una situación real de ETL donde puedan llegar a aparecer 
  duplicados, nulos y valores atípicos durante la ingesta- Transformación- 
  Carga de la data.

## Correr la solución

El archivo `main.py` contiene la solución y hace uso del archivo de requerimientos
`requirements.txt`.

```shell
git clone https://github.com/000paradox000/coderhouse-de-preentrega-2.git
cd coderhouse-de-preentrega-2
# hacer una copia del archivo env.example, llamarlo .env y reemplazar los valores
python3 -m venv .venv
.venv\bin\activate
pip install -r requirements.txt
python main.py
```
