"""Módulo 0: perfil del inversionista (lo que el usuario elige en la app)."""
from dataclasses import dataclass

OBJETIVOS = ("crecimiento", "dividendos", "swing", "aprendizaje")
RIESGOS = ("baja", "media", "alta")
EXPERIENCIAS = ("principiante", "intermedio", "avanzado")

# Pesos de la puntuación fundamental según el objetivo (cada fila suma 1.0)
PESOS_FUNDAMENTALES = {
    "crecimiento": {"crecimiento": 0.30, "rentabilidad": 0.25, "deuda": 0.15, "flujo": 0.15, "valoracion": 0.15},
    "dividendos":  {"crecimiento": 0.10, "rentabilidad": 0.20, "deuda": 0.20, "flujo": 0.30, "valoracion": 0.20},
    "swing":       {"crecimiento": 0.20, "rentabilidad": 0.20, "deuda": 0.20, "flujo": 0.20, "valoracion": 0.20},
    "aprendizaje": {"crecimiento": 0.20, "rentabilidad": 0.25, "deuda": 0.20, "flujo": 0.20, "valoracion": 0.15},
}


@dataclass
class PerfilInversionista:
    objetivo: str
    horizonte_anios: int
    tolerancia_riesgo: str
    max_caida_tolerada: float  # 0.15 = 15%
    capital_inicial: float
    aporte_mensual: float
    experiencia: str

    def __post_init__(self):
        if self.objetivo not in OBJETIVOS:
            raise ValueError(f"objetivo debe ser uno de {OBJETIVOS}")
        if self.tolerancia_riesgo not in RIESGOS:
            raise ValueError(f"tolerancia_riesgo debe ser una de {RIESGOS}")
        if self.experiencia not in EXPERIENCIAS:
            raise ValueError(f"experiencia debe ser una de {EXPERIENCIAS}")
        if not 0 < self.max_caida_tolerada <= 1:
            raise ValueError("max_caida_tolerada debe estar entre 0 y 1")
        if self.horizonte_anios <= 0 or self.capital_inicial < 0 or self.aporte_mensual < 0:
            raise ValueError("horizonte, capital y aporte deben ser valores válidos")


def evaluar_compatibilidad(perfil: PerfilInversionista, metricas: dict) -> list[str]:
    """Compara métricas de un instrumento con los límites del usuario.
    Es información, no una recomendación de compra."""
    notas = []
    dd = abs(metricas.get("max_drawdown", 0))
    if dd > perfil.max_caida_tolerada:
        notas.append(f"Su caída máxima histórica ({dd:.0%}) supera tu límite ({perfil.max_caida_tolerada:.0%}).")
    return notas
