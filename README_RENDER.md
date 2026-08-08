# Kalshi BTC 15m Bot — fixed build

Cambios realizados:
- Dependencias actualizadas para Python 3.13:
  - numpy 2.1.3
  - pandas 2.2.3
- Eliminada la importación duplicada de `calculate_indicators` en `app.py`.
- Se conserva la estructura original del bot y su estrategia.

Nota:
Este build sigue usando las fuentes de precio que ya tenía el proyecto. No se modificó
la fuente de datos de Kalshi ni la lógica de señales sin probarla primero.
