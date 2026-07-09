"""Tests del ruteo de modelos."""

from __future__ import annotations

from gateway.router import route


def test_tarea_simple_va_a_barato():
    tier, model = route("hola, gracias")
    assert tier == "cheap" and model == "claude-haiku-4-5"


def test_tarea_compleja_va_a_caro():
    tier, model = route("analiza y compara paso a paso estas dos opciones")
    assert tier == "expensive" and model == "claude-sonnet-5"


def test_prompt_largo_va_a_caro():
    tier, _ = route("x" * 300)
    assert tier == "expensive"


def test_force_overridea_la_heuristica():
    tier, model = route("analiza esto complejo", force="cheap")
    assert tier == "cheap" and model == "claude-haiku-4-5"
