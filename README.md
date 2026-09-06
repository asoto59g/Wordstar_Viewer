<img width="1292" height="218" alt="image" src="https://github.com/user-attachments/assets/50eb3190-a0f6-48a9-b152-20100f150466" />


# Visor WordStar


[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Formato](https://img.shields.io/badge/formato-WordStar%20DOS-6B7280)](https://www.both.org/?p=6898)

Aplicacion Streamlit para consultar documentos WordStar antiguos, incluidos los archivos sin extension de esta carpeta.

App en siguiente link: https://wordstarviewer-fbeghpk9ynug5oscgsuf2v.streamlit.app/

La aplicacion interpreta los controles inline de WordStar, conserva el espaciado de los documentos y permite descargar una copia de texto limpio. Los archivos `CHAPIA91`, `DOCTOP`, `NAVA`, `RABA`, `RABAZO2` y `RABAZO3` son documentos de datos y deben permanecer junto a `app.py`.

## Ejecutar

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Publicar en GitHub

1. Crea un repositorio nuevo y sube todo el contenido de esta carpeta, incluidos los seis archivos sin extension.
2. En [Streamlit Community Cloud](https://share.streamlit.io/), selecciona **Deploy an app**.
3. Elige el repositorio, la rama y `app.py` como archivo principal.
4. Pulsa **Deploy**. Streamlit instalara automaticamente `requirements.txt`.

Los comandos de punto, como `.LH` y `.CW`, se muestran en la vista pero no se interpretan como maquetacion de pagina. La referencia del formato es el articulo [Converting WordStar files](https://www.both.org/?p=6898).

## Estructura

| Archivo | Funcion |
| --- | --- |
| `app.py` | Interfaz Streamlit y seleccion de documentos |
| `wordstar_viewer.py` | Decodificacion y renderizado seguro |
| `CHAPIA91`, `DOCTOP`, `NAVA`, `RABA`, `RABAZO2`, `RABAZO3` | Documentos WordStar originales |
| `requirements.txt` | Dependencia de despliegue |
