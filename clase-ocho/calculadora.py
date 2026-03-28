"""
Operaciones aritméticas básicas con validación de operandos.

Se aceptan ``int`` y ``float`` finitos (``bool`` cuenta como ``int`` en Python).
Se rechazan ``NaN``, infinitos y demás tipos no numéricos.
"""

from __future__ import annotations

import math

__all__ = ["PI", "sumar", "restar", "multiplicar", "dividir"]

# Precisión doble IEEE 754 ~ π (uso general en cálculos)
PI: float = math.pi

type Numero = int | float


def _validar_operando(valor: Numero, nombre: str) -> Numero:
    """
    Valida un operando numérico finito.

    Raises
    ------
    TypeError
        Si el tipo no es ``int`` ni ``float``.
    ValueError
        Si el flotante es ``nan`` o infinito.
    """
    if isinstance(valor, int):
        return valor
    if isinstance(valor, float):
        if math.isnan(valor):
            raise ValueError(f"{nombre}: no se acepta float('nan').")
        if math.isinf(valor):
            raise ValueError(f"{nombre}: no se aceptan infinitos.")
        return valor
    raise TypeError(
        f"{nombre}: se esperaba int o float, no {type(valor).__name__!r}."
    )


def _validar_par(a: Numero, b: Numero) -> tuple[Numero, Numero]:
    return _validar_operando(a, "a"), _validar_operando(b, "b")


def sumar(a: Numero, b: Numero) -> float:
    """Suma ``a`` y ``b`` con validación de operandos."""
    x, y = _validar_par(a, b)
    try:
        r = float(x) + float(y)
    except OverflowError as exc:
        raise OverflowError("sumar: desbordamiento al sumar los operandos.") from exc
    if math.isinf(r) or math.isnan(r):
        raise OverflowError("sumar: el resultado no es un número finito representable.")
    return r


def restar(a: Numero, b: Numero) -> float:
    """Resta ``b`` de ``a`` con validación de operandos."""
    x, y = _validar_par(a, b)
    try:
        r = float(x) - float(y)
    except OverflowError as exc:
        raise OverflowError("restar: desbordamiento al restar.") from exc
    if math.isinf(r) or math.isnan(r):
        raise OverflowError("restar: el resultado no es un número finito representable.")
    return r


def multiplicar(a: Numero, b: Numero) -> float:
    """Producto de ``a`` y ``b`` con validación de operandos."""
    x, y = _validar_par(a, b)
    try:
        r = float(x) * float(y)
    except OverflowError as exc:
        raise OverflowError("multiplicar: desbordamiento en la multiplicación.") from exc
    if math.isinf(r) or math.isnan(r):
        raise OverflowError("multiplicar: el resultado no es un número finito representable.")
    return r


def dividir(a: Numero, b: Numero) -> float:
    """
    Cociente ``a / b`` con validación y comprobación de división por cero.

    Raises
    ------
    ZeroDivisionError
        Si ``b`` es cero (entero o flotante).
    """
    x, y = _validar_par(a, b)
    fy = float(y)
    if fy == 0.0:
        raise ZeroDivisionError("dividir: el divisor no puede ser cero.")
    try:
        r = float(x) / fy
    except OverflowError as exc:
        raise OverflowError("dividir: desbordamiento en la división.") from exc
    if math.isinf(r) or math.isnan(r):
        raise OverflowError("dividir: el resultado no es un número finito representable.")
    return r
