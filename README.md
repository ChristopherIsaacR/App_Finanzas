# Stock Market Intelligence

Plataforma personal de análisis bursátil (Etapa 1: datos). No ejecuta operaciones ni da recomendaciones de compra.

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
## en power shell se debera usar .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Descargar datos
```bash
cd backend
python -m app.cli MSFT AAPL VOO --period 5y
```
Los datos se guardan en `data/market.db` (SQLite). Para PostgreSQL, define `DATABASE_URL` en `.env`.

## Pruebas
```bash
cd backend && pytest
# En powershell asi deberia de ser
cd backend
pytest
```

## Reglas del proyecto
1. No usar dinero real durante el desarrollo y la validación.
2. Ninguna salida del sistema es garantía de rentabilidad.
3. Sin operaciones automáticas en GBM.
