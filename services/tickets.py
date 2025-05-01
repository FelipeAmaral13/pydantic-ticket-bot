from datetime import datetime
from utils.logger import log_info, log_warning, log_error

def consultar_ticket(db, ticket_id: str):
    try:
        cur = db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cur.fetchone()
        if row:
            log_info(f"Ticket encontrado: ID {row[0]}, Resumo: {row[1]}, Severidade: {row[2]}, Departamento: {row[3]}, Status: {row[4]}")
            return {
                "ID": row[0],
                "Resumo": row[1],
                "Severidade": row[2],
                "Departamento": row[3],
                "Categoria": row[4],
                "Status": row[5],
                "Criado em": row[6],
                "Fechado em": row[7] if row[7] else "—"
            }
        else:
            log_warning(f"Ticket não encontrado: {ticket_id}")
            return None
    except Exception as e:
        log_error(f"Erro ao consultar ticket {ticket_id}: {e}")
        return None

def listar_tickets_abertos(db):
    try:
        cur = db.execute("""
            SELECT ticket_id, summary, severity, department, category, status, created_at, closed_at 
            FROM tickets 
            WHERE status = 'open'
        """)
        rows = cur.fetchall()
        if not rows:
            log_info("Nenhum ticket aberto no momento.")
            return []
        return [
            {
                "ID": row[0],
                "Resumo": row[1],
                "Severidade": row[2],
                "Departamento": row[3],
                "Categoria": row[4],
                "Status": row[5],
                "Criado em": row[6],
                "Fechado em": row[7] if row[7] else "—"
            }
            for row in rows
        ]

    except Exception as e:
        log_error(f"Erro ao listar tickets abertos: {e}")
        return []

def encerrar_ticket(db, ticket_id: str) -> bool:
    try:
        closed_at = datetime.now().isoformat()
        db.execute(
            "UPDATE tickets SET status = ?, closed_at = ? WHERE ticket_id = ?",
            ("closed", closed_at, ticket_id)
        )
        db.commit()
        log_info(f"✅ Ticket encerrado: {ticket_id} em {closed_at}")
        return True
    except Exception as e:
        log_error(f"❌ Erro ao encerrar ticket {ticket_id}: {e}")
        return False