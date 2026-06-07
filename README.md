# ai-engineering-lab

Repositorio de practicas para AI Engineering con una estructura simple en Python y una convencion de ramas orientada a sesiones.

## Estructura

- `app/`: codigo fuente principal.
- `docs/`: documentacion tecnica y de arquitectura.
- `scripts/`: utilidades de soporte para el flujo del repositorio.

## Setup rapido

El entorno objetivo es `WSL Ubuntu` con `Python 3.12+`.

```bash
sudo apt install python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
```

Crea tu archivo `.env` a partir de `.env.example` y define `OPENAI_API_KEY`.

## Buenas practicas

- No subir `.env` ni credenciales reales.
- No incluir datos personales ni informacion sensible.
- Usar datos ficticios o anonimizados.
- Mantener documentadas arquitectura, decisiones y limitaciones.

## Flujo Git por sesion

La convencion recomendada es crear una rama por hito de sesion:

- `pre-session-N`: estado base antes de empezar la sesion `N`.
- `session-N`: trabajo realizado durante la sesion `N`.
- `post-session-N`: estado final o limpieza posterior, si hace falta.

Ejemplo:

```text
main
pre-session-1
session-1
pre-session-2
session-2
```

Si lo que ahora tienes subido representa el punto de partida de la primera sesion, la rama correcta es `pre-session-1`.

Puedes crear ramas con el helper del repo:

```bash
python3 scripts/create_session_branch.py --phase pre --number 1
python3 scripts/create_session_branch.py --phase session --number 1 --base pre-session-1
```

Mas detalle en [docs/git-workflow.md](/home/maae/projects/personal/ai-engineering-lab/docs/git-workflow.md).

## Documentacion tecnica

- Arquitectura: [docs/architecture.md](/home/maae/projects/personal/ai-engineering-lab/docs/architecture.md)
- Flujo Git: [docs/git-workflow.md](/home/maae/projects/personal/ai-engineering-lab/docs/git-workflow.md)
