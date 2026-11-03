import pytest

from app.analysis.profile import PerfilInversionista, evaluar_compatibilidad


def _perfil(**kw):
    base = dict(objetivo="crecimiento", horizonte_anios=5, tolerancia_riesgo="media",
                max_caida_tolerada=0.15, capital_inicial=5000, aporte_mensual=1000, experiencia="principiante")
    base.update(kw)
    return PerfilInversionista(**base)


def test_alerta_drawdown():
    assert evaluar_compatibilidad(_perfil(), {"max_drawdown": -0.35})
    assert not evaluar_compatibilidad(_perfil(), {"max_drawdown": -0.10})


def test_validacion():
    with pytest.raises(ValueError):
        _perfil(objetivo="otro")
