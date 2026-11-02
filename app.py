"""Streamlit web UI. Run from the repository root:  streamlit run app.py

Uses exactly the same `Pipeline.search` as the CLI (src/cli.py `search`).
Config path can be overridden with the CIA_CONFIG environment variable.
"""

from __future__ import annotations

import os

import streamlit as st

from src.pipeline import DISCLAIMER, Pipeline, PipelineError

CONFIG = os.environ.get("CIA_CONFIG", "configs/final.yaml")


@st.cache_resource(show_spinner="Loading contracts and building the index...")
def get_pipeline(config_path: str) -> Pipeline:
    return Pipeline.from_config(config_path)


def run_query(pipeline: Pipeline, query: str, top_k: int):
    """Thin wrapper (kept separate so tests can exercise the UI path without a browser)."""
    return pipeline.search(query, top_k=top_k)


def main() -> None:
    st.set_page_config(page_title="Contract Intelligence Assistant", layout="wide")
    st.title("Contract Intelligence Assistant")
    st.caption(DISCLAIMER)

    try:
        pipeline = get_pipeline(CONFIG)
    except PipelineError as e:
        st.error(f"Data/index not available: {e}")
        st.info("Run `python -m src.cli prepare-data --source <legalbench-rag root>` first.")
        return
    except Exception as e:  # pragma: no cover - surfaced to the user without a traceback dump
        st.error(f"Could not load the pipeline ({type(e).__name__}). Check the config file: {CONFIG}")
        return

    with st.sidebar:
        st.markdown(f"**Config:** `{pipeline.cfg.get('name')}` ({pipeline.cfg.get('status')})")
        st.markdown(f"**Indexed contracts:** {len(pipeline.documents)}  \n**Chunks:** {len(pipeline.index.chunks)}")
        top_k = st.slider("Passages to return (top-k)", 1, 20, 5)
        with st.expander("Indexed documents"):
            for d in sorted(pipeline.documents):
                st.text(d)

    with st.form("search"):
        query = st.text_area("Ask a question about the contracts",
                             placeholder="e.g. Consider the ... Agreement between X and Y; "
                                         "What restrictions apply to sublicensing?")
        submitted = st.form_submit_button("Search")
    if not submitted:
        return
    if not query.strip():
        st.warning("Please enter a question.")
        return
    try:
        res = run_query(pipeline, query, top_k)
    except PipelineError as e:
        st.error(str(e))
        return
    except Exception as e:  # pragma: no cover
        st.error(f"Search failed ({type(e).__name__}).")
        return

    st.markdown(f"**Query:** {res.query}")
    sv = "n/a" if res.signal_value is None else f"{res.signal_value:.4f}"
    if res.abstained:
        st.warning(f"**Abstained** - no sufficiently relevant evidence in the indexed contracts "
                   f"(`{res.signal}` = {sv} < threshold {res.threshold:.4f}; reason: {res.abstention_reason}).")
        return
    st.success(f"Found {len(res.passages)} passage(s)  (`{res.signal}` = {sv} >= threshold {res.threshold:.4f})")
    for p in res.passages:
        with st.container(border=True):
            st.markdown(f"**#{p['rank']}** &nbsp; score `{p['score']:.4f}` &nbsp; "
                        f"offsets `[{p['start_offset']}, {p['end_offset']})`")
            st.caption(p["document_id"])
            st.text(p["text"])


if __name__ == "__main__":
    main()
