from pathlib import Path

import streamlit as st

from wordstar_viewer import plain_text, read_source, render_html


ROOT = Path(__file__).parent
LOCAL_FILES = sorted(path for path in ROOT.iterdir() if path.is_file() and path.name not in {"app.py", "wordstar_viewer.py", "README.md", "requirements.txt"})

st.set_page_config(page_title="Visor WordStar", page_icon="WS", layout="wide")
st.markdown(
    """
    <style>
    :root { --ink: #17212b; --paper: #fffdf7; --accent: #c4522d; --line: #d9d2c3; }
    .stApp { background: #f1ede3; color: var(--ink); }
    .block-container { max-width: 1220px; padding-top: 2.2rem; }
    h1, h2, h3 { font-family: Georgia, serif; letter-spacing: 0; }
    .ws-paper { background: var(--paper); border: 1px solid var(--line); border-top: 5px solid var(--accent); padding: 2.3rem 3rem; min-height: 460px; box-shadow: 0 12px 30px rgba(23,33,43,.08); font-family: "Courier New", monospace; font-size: 15px; line-height: 1.55; white-space: normal; overflow-wrap: anywhere; }
    .ws-control, .ws-space, .ws-page { color: var(--accent); font-size: .78em; font-weight: bold; }
    .ws-dot-hidden { color: #9d978d; }
    .ws-caption { color: #6a6359; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Visor de documentos WordStar")
st.caption("Recupera documentos antiguos de los anos 1990-1991 sin alterar los archivos originales.")

with st.sidebar:
    st.header("Abrir documento")
    choices = [path.name for path in LOCAL_FILES]
    selected = st.selectbox("Archivo local", choices, index=0 if choices else None)
    uploaded = st.file_uploader("O subir un archivo WordStar", type=None)
    st.divider()
    encoding = st.selectbox("Codificacion", ["cp437", "latin-1", "utf-8"], index=0)
    strip_high_bit = st.checkbox("Ignorar bit alto de microjustificacion", value=True)
    show_controls = st.checkbox("Mostrar marcas de control", value=False)
    show_dot_commands = st.checkbox("Mostrar comandos . de WordStar", value=True)

if uploaded is not None:
    source_name = uploaded.name
    source = uploaded
elif selected:
    source_name = selected
    source = (ROOT / selected).read_bytes()
else:
    st.warning("No hay archivos WordStar en esta carpeta.")
    st.stop()

try:
    decoded, byte_count = read_source(source, encoding, strip_high_bit)
except (OSError, UnicodeError) as error:
    st.error(f"No se pudo leer el documento: {error}")
    st.stop()

st.subheader(source_name)
metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Bytes", f"{byte_count:,}")
metric_b.metric("Caracteres", f"{len(decoded):,}")
metric_c.metric("Lineas", f"{decoded.count(chr(10)) + 1:,}")

rendered = render_html(decoded, show_controls, show_dot_commands)
preview_tab, source_tab = st.tabs(["Vista de documento", "Texto y diagnostico"])
with preview_tab:
    st.markdown(f'<div class="ws-paper">{rendered}</div>', unsafe_allow_html=True)
with source_tab:
    st.text_area("Texto decodificado", decoded, height=430)
    st.caption("Los controles WordStar se conservan para la vista HTML; el texto descargable los elimina.")

download_col, info_col = st.columns([1, 3])
with download_col:
    st.download_button(
        "Descargar texto limpio",
        data=plain_text(decoded).encode("utf-8"),
        file_name=f"{Path(source_name).stem}.txt",
        mime="text/plain",
        use_container_width=True,
    )
with info_col:
    st.markdown('<div class="ws-caption">Formato reconocido: ASCII/CP437, CR-LF, EOF 0x1A, negrita, cursiva, subrayado, tachado, superindice y subindice.</div>', unsafe_allow_html=True)