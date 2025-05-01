
from pydantic_graph import BaseNode, GraphRunContext, Graph, End

from services.state import State
from agents.classification import agent_classify
from agents.creation import agent_create
from utils.logger import log_info, log_debug, log_warning, log_error

class GetTicketInfo(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "ClassifyTicket":
        try:
            if not ctx.state.summary:
                raise ValueError("Resumo do problema não fornecido no estado.")
        except Exception as e:
            log_error(f"❌ Erro ao coletar o resumo do problema: {e}")
            raise
        return ClassifyTicket()

class ClassifyTicket(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "CreateTicket":
        log_info(f"🔍 Classificando ticket com base no resumo: '{ctx.state.summary}'")
        try:
            result = await agent_classify.run(
                f"Classifique o seguinte problema: {ctx.state.summary}",
                deps=ctx.state
            )
            ctx.state.severity = result.output.severity
            ctx.state.department = result.output.department
            ctx.state.category = result.output.category
            log_info(f"📊 Classificação concluída - Severidade: {ctx.state.severity}, Departamento: {ctx.state.department}")
        except Exception as e:
            log_error(f"❌ Erro ao classificar ticket: {e}")
            raise
        return CreateTicket()

class CreateTicket(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "GetStatus":
        log_info(f"Iniciando criação do ticket para: resumo='{ctx.state.summary}', severidade='{ctx.state.severity}', departamento='{ctx.state.department}', categoria='{ctx.state.category}'")
        try:
            result = await agent_create.run(
                f"Criar ticket: {ctx.state.summary}, severidade: {ctx.state.severity}, departamento: {ctx.state.department}, categoria: {ctx.state.category}",
                deps=ctx.state
            )
            ctx.state.ticket_id = result.output.ticket_id
            ctx.state.created_at = result.output.created_at
            ctx.state.closed_at = result.output.closed_at
            log_info(f"✅ Ticket criado com sucesso: ID={ctx.state.ticket_id}")
        except Exception as e:
            log_error(f"❌ Erro ao criar ticket: {e}")
            raise
        return GetStatus()


class GetStatus(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "End":
        log_debug(f"Consultando status do ticket: ID={ctx.state.ticket_id}")
        try:
            cur = ctx.state.db.execute(
                "SELECT status FROM tickets WHERE ticket_id = ?",
                (ctx.state.ticket_id,)
            )
            row = cur.fetchone()
            ctx.state.status = row[0] if row else "not_found"
            if row:
                log_info(f"📌 Status do ticket {ctx.state.ticket_id}: {ctx.state.status}")
            else:
                log_warning(f"⚠️ Ticket {ctx.state.ticket_id} não encontrado no banco.")
        except Exception as e:
            log_error(f"❌ Erro ao consultar status do ticket {ctx.state.ticket_id}: {e}")
            raise
        return End(f"Ticket {ctx.state.ticket_id} status: {ctx.state.status}")

graph = Graph(nodes=[GetTicketInfo, ClassifyTicket, CreateTicket, GetStatus])