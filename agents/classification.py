from pydantic import BaseModel
from typing import Literal
from pydantic_ai import Agent

from services.state import State

class ClassificationOutput(BaseModel):
    severity: Literal["low", "medium", "high"]
    department: Literal["TI", "Secretaria", "Coordenação"]
    category: Literal["rede", "hardware", "sistema", "email", "segurança", "outros"]


agent_classify = Agent(
    'groq:meta-llama/llama-4-scout-17b-16e-instruct',
    deps_type=State,
    output_type=ClassificationOutput,
    system_prompt="""
        Você é um assistente responsável por classificar chamados de suporte.
        Com base no texto do problema, determine:
        - o nível de severidade: 'low', 'medium' ou 'high'
        - o departamento responsável: 'TI', 'Secretaria' ou 'Coordenação'
        - a categoria do problema: 'rede', 'hardware', 'sistema', 'email', 'segurança' ou 'outros'
    """
)
