from pydantic import BaseModel
from typing import Literal
from pydantic_ai import Agent, RunContext
import uuid
from datetime import datetime


from services.state import State

class CreateTicketOutput(BaseModel):
    ticket_id: str
    summary: str
    severity: Literal["low", "medium", "high"]
    department: str
    category: str
    status: Literal["open"]
    created_at: str
    closed_at: str | None = None


agent_create = Agent(
    'groq:meta-llama/llama-4-scout-17b-16e-instruct',
    deps_type=State,
    output_type=CreateTicketOutput,
    system_prompt="Você é um assistente para criação de tickets."
)

@agent_create.tool
async def create_ticket(ctx: RunContext[State], summary: str, severity: str, department: str, category: str) -> CreateTicketOutput:
    ticket_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    ctx.deps.db.execute(
        "INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?)",
        (ticket_id, summary, severity, department, category, "open", created_at, None)
    )
    ctx.deps.db.commit()
    return CreateTicketOutput(
        ticket_id=ticket_id,
        summary=summary,
        severity=severity,
        department=department,
        category=category,
        status="open",
        created_at=created_at,
        closed_at=None
    )