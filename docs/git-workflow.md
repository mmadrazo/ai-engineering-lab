# Flujo de ramas por sesion

## Objetivo

Mantener un historial facil de seguir creando ramas por cada sesion del laboratorio.

## Convencion

- `main`: rama estable o de referencia general.
- `pre-session-N`: snapshot antes de empezar la sesion `N`.
- `session-N`: trabajo de la sesion `N`.
- `post-session-N`: ajustes finales, resumen o limpieza despues de la sesion `N`.

`N` debe ser un entero positivo: `1`, `2`, `3`, etc.

## Flujo recomendado

Para una nueva sesion `2`:

1. Congelar el punto de partida:

   ```bash
   git branch pre-session-2
   ```

2. Crear la rama de trabajo:

   ```bash
   git checkout -b session-2 pre-session-2
   ```

3. Trabajar y hacer commits normalmente en `session-2`.

4. Si quieres dejar un estado de cierre separado:

   ```bash
   git branch post-session-2
   ```

## Helper incluido

El script `scripts/create_session_branch.py` valida nombres y ejecuta la creacion de ramas:

```bash
python3 scripts/create_session_branch.py --phase pre --number 2
python3 scripts/create_session_branch.py --phase session --number 2 --base pre-session-2
python3 scripts/create_session_branch.py --phase post --number 2 --base session-2
```

Por defecto el script crea la rama sin cambiar tu `HEAD`. Si quieres moverte a ella:

```bash
python3 scripts/create_session_branch.py --phase session --number 2 --base pre-session-2 --checkout
```

## Caso actual del repo

Si el contenido que ya esta publicado corresponde al estado previo a la primera sesion, la rama que debe apuntar a ese commit es:

```text
pre-session-1
```
