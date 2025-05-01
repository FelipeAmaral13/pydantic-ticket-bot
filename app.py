import streamlit as st
import asyncio
import pandas as pd

from services.state import State
from db.database import DatabaseConnection
from graph.nodes import GetTicketInfo, graph
from services.tickets import consultar_ticket, listar_tickets_abertos, encerrar_ticket

st.set_page_config(page_title="Gerenciador de Tickets", layout="centered")

db_conn = DatabaseConnection.get_instance().get_connection()

st.sidebar.title("📋 Menu de Tickets")
opcao = st.sidebar.radio("Escolha uma opção:", [
    "Registrar novo ticket",
    "Consultar ticket existente",
    "Listar tickets abertos"
])

if opcao == "Registrar novo ticket":
    st.header("📝 Novo Ticket")
    resumo = st.text_area("Descreva o problema")
    if st.button("Enviar"):
        async def criar_ticket(summary):
            state = State(db=db_conn, summary=summary)
            result = await graph.run(GetTicketInfo(), state=state)
            st.success("✅ Ticket criado com sucesso!")
            st.json({
                "ticket_id": state.ticket_id,
                "status": state.status,
                "severidade": state.severity,
                "departamento": state.department,
                "categoria": state.category,
                "criado_em": state.created_at,
                "fechado_em": state.closed_at
            })
        asyncio.run(criar_ticket(resumo))

elif opcao == "Consultar ticket existente":
    st.header("🔍 Consultar Ticket")
    ticket_id = st.text_input("Digite o ID do ticket")
    if st.button("Buscar"):
        resultado = consultar_ticket(db_conn, ticket_id)
        if resultado:
            st.success("Ticket encontrado:")
            st.json(resultado)
            if resultado["Status"] != "closed":
                if st.button("Encerrar Ticket"):
                    sucesso = encerrar_ticket(db_conn, ticket_id)
                    if sucesso:
                        st.success("✅ Ticket encerrado com sucesso!")
                        resultado = consultar_ticket(db_conn, ticket_id)  # <-- recarrega
                        st.json(resultado)
                    else:
                        st.error("❌ Erro ao encerrar o ticket.")   
        else:
            st.warning("Ticket não encontrado.")

elif opcao == "Listar tickets abertos":
    st.header("📂 Tickets Abertos")
    resultados = listar_tickets_abertos(db_conn)
    
    if resultados:
        for ticket in resultados:
            with st.expander(f"🔎 Ticket {ticket['ID']} - {ticket['Resumo'][:40]}..."):
                st.write(f"**Severidade:** {ticket['Severidade']}")
                st.write(f"**Departamento:** {ticket['Departamento']}")
                st.write(f"**Categoria:** {ticket['Categoria']}")
                st.write(f"**Status:** {ticket['Status']}")
                st.write(f"**Criado em:** {ticket['Criado em']}")
                st.write(f"**Fechado em:** {ticket['Fechado em']}")

                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"Encerrar {ticket['ID']}", key=f"encerrar_{ticket['ID']}"):
                        sucesso = encerrar_ticket(db_conn, ticket['ID'])
                        if sucesso:
                            st.success("✅ Ticket encerrado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao encerrar o ticket.")
    else:
        st.info("Nenhum ticket aberto no momento.")

