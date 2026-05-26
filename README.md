# ai-engineering-lab
# Buenas prácticas obligatorias

Para todos los repositorios, especialmente los públicos, se deben cumplir las siguientes prácticas:

- No incluir archivos `.env` en el repositorio.
- No exponer claves API, tokens, contraseñas o credenciales.
- No incluir datos reales de usuarios o información personal.
- Utilizar `.env.example` para documentar las variables necesarias.
- Emplear datos ficticios o anonimizados.
- Incluir un `README` técnico con:
  - Setup
  - Arquitectura
  - Decisiones de diseño
  - Limitaciones del sistema

## Requisitos adicionales para AI Engineering

- Documentar la arquitectura del sistema:
  - CAG
  - RAG
  - Agentes
  - Otros componentes relevantes

- Explicar cómo se gestiona:
  - Latencia
  - Coste
  - Calidad (evaluación)
  - Seguridad (guardrails)

- Incluir trazabilidad básica:
  - Logs
  - Debugging
  - Evaluación (si aplica)

# Primer paso: configurar el entorno
El entorno de desarrollo será **WSL Ubuntu** y **Python**. Para ello, se requiere configurar el entorno siguiendo los siguientes pasos:
1. Instalar Python y `pip`:
   sudo apt install python3-pip
 
2. Instalar las librerías necesarias:
   pip3 install openai python-dotenv
 
3. Crear el entorno virtual:
   python3 -m venv .venv
 
4. Activar el entorno virtual:
   source .venv/bin/activate
 
5. Instalar las librerías de OpenAI dentro del entorno virtual:
   pip install openai python-dotenv
 

 # Segundo paso: Generar el API Key en ChatGPT
 - Generar tu API key


 # Tercer paso: Ejecutar una llamada a la API
- Ejecutar una llamada básica


- Instalar dependencias para poder cargar la información del entorno y ponder hacer uso del API de OpenAI
- pip install python-dotenv openai