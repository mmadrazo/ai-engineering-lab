from __future__ import annotations

import time
from typing import Iterable, cast

import streamlit as st

from app.context.examples import format_examples_for_prompt, select_examples
from app.schemas.estimation import ExampleFormat, PreprocessingMode
from app.services.llm_service import build_system_prompt
from web.client import BackendClientError, BackendConfig, build_payload, estimate_software_project


st.set_page_config(
    page_title="Estimator CAG",
    page_icon="💬",
    layout="wide",
)


def render_estimation_text(text: str) -> None:
    """Stream the estimation progressively using the placeholder + delta pattern."""
    placeholder = st.empty()
    buffer = ""

    def token_stream() -> Iterable[str]:
        for part in text.split():
            yield part + " "
            time.sleep(0.012)

    for chunk in token_stream():
        buffer += chunk
        placeholder.markdown(buffer)


def main() -> None:
    st.title("Estimator CAG")
    st.caption("Pega una transcripción de reunión y obtén la estimación generada por el backend.")

    with st.sidebar:
        st.header("Conexión")
        backend_url = st.text_input("Backend URL", value="http://localhost:8000")
        st.divider()
        st.header("CAG")
        preprocessing = st.selectbox(
            "Preprocessing",
            cast(tuple[PreprocessingMode, ...], ("none", "inline_cleaning", "two_phase")),
            index=0,
        )
        example_format = st.selectbox(
            "Example format",
            cast(tuple[ExampleFormat, ...], ("markdown", "json", "narrative")),
            index=0,
        )
        use_examples = st.checkbox("Use examples", value=True)
        num_examples = st.slider("Number of examples", min_value=0, max_value=5, value=3)
        model = st.text_input("Model override", value="")
        max_tokens = st.number_input("Max tokens", min_value=256, max_value=16000, value=4000, step=256)
        thinking_budget = st.number_input(
            "Thinking budget",
            min_value=0,
            max_value=16000,
            value=0,
            step=256,
            help="Use 0 to leave it unset.",
        )
        evaluate = st.checkbox("Run evaluation", value=True)

        system_prompt = build_system_prompt(
            example_format=example_format,
            num_examples=int(num_examples),
            use_examples=use_examples,
            inline_cleaning=(preprocessing == "inline_cleaning"),
        )
        context_examples = format_examples_for_prompt(
            select_examples(int(num_examples)) if use_examples else [],
            fmt=example_format,
        )

        st.divider()
        st.header("System prompt")
        st.text_area("Active system prompt", value=system_prompt, height=260, disabled=True)
        st.header("Static CAG context")
        st.text_area("Injected examples", value=context_examples or "No examples injected.", height=280, disabled=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Pega la transcripción y te devolveré la estimación en un chat conversacional.",
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    transcript = st.chat_input("Pega aquí la transcripción de la reunión")

    if not transcript:
        st.stop()

    st.session_state.messages.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.markdown(transcript)

    payload = build_payload(
        transcription=transcript,
        preprocessing=preprocessing,
        example_format=example_format,
        num_examples=int(num_examples),
        use_examples=use_examples,
        model=model.strip() or None,
        max_tokens=int(max_tokens),
        thinking_budget=int(thinking_budget) if thinking_budget else None,
        evaluate=evaluate,
    )

    with st.chat_message("assistant"):
        status = st.status("Generando estimación...", expanded=True)
        try:
            response = estimate_software_project(BackendConfig(base_url=backend_url), payload)
            status.update(label="Estimación recibida", state="complete")
        except BackendClientError as exc:
            status.update(label="No se pudo conectar con el backend", state="error")
            st.error(str(exc))
            return

        metrics = response.get("usage", {})
        st.caption(
            "Modelo: {model} | Entrada: {inp} tokens | Salida: {out} tokens | Latencia: {lat} ms".format(
                model=response.get("model", "unknown"),
                inp=metrics.get("input_tokens", 0),
                out=metrics.get("output_tokens", 0),
                lat=response.get("latency_ms", 0),
            )
        )
        st.subheader("Estimación")
        render_estimation_text(response["estimation"])

        with st.expander("Detalles técnicos", expanded=False):
            st.json(
                {
                    "model": response.get("model"),
                    "provider": response.get("provider"),
                    "finish_reason": response.get("finish_reason"),
                    "latency_ms": response.get("latency_ms"),
                    "usage": response.get("usage"),
                    "preprocessing": response.get("preprocessing"),
                }
            )
            if response.get("validation") is not None:
                st.json(response["validation"])
            if response.get("extracted_requirements"):
                st.markdown("### Requisitos extraídos")
                st.code(response["extracted_requirements"], language="markdown")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response["estimation"],
            }
        )


if __name__ == "__main__":
    main()
