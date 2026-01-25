"""
SIPI UI Prototype - Streamlit App
Prototipo de interfaz para validar mejoras de UI
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/sipi")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Page config
st.set_page_config(
    page_title="SIPI - Sistema de Procesos",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for status colors
st.markdown("""
<style>
.status-documentado {
    color: #10B981;
    font-weight: bold;
}
.status-parcial {
    color: #F59E0B;
    font-weight: bold;
}
.status-no-documentado {
    color: #EF4444;
    font-weight: bold;
}
.timeline-item {
    border-left: 3px solid #3B82F6;
    padding-left: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def get_status_class(status):
    """Get CSS class for documentation status"""
    if status == "DOCUMENTADO":
        return "status-documentado"
    elif status == "PARCIALMENTE_DOCUMENTADO":
        return "status-parcial"
    else:
        return "status-no-documentado"

def get_status_icon(status):
    """Get icon for documentation status"""
    if status == "DOCUMENTADO":
        return "✅"
    elif status == "PARCIALMENTE_DOCUMENTADO":
        return "⚠️"
    else:
        return "❌"

def main():
    st.title("🏛️ SIPI - Sistema de Procesos y Documentación")

    # Sidebar navigation
    st.sidebar.title("Navegación")
    page = st.sidebar.radio(
        "Seleccionar vista:",
        ["Dashboard", "Inmuebles", "Procesos", "Configuración"]
    )

    if page == "Dashboard":
        show_dashboard()
    elif page == "Inmuebles":
        show_inmuebles()
    elif page == "Procesos":
        show_procesos()
    elif page == "Configuración":
        show_configuracion()

def show_dashboard():
    st.header("📊 Dashboard de Procesos y Documentación")

    # Get summary stats
    try:
        with SessionLocal() as session:
            # Total inmuebles
            result = session.execute(text("SELECT COUNT(*) FROM inmuebles"))
            total_inmuebles = result.scalar()

            # Procesos por estado
            result = session.execute(text("""
                SELECT
                    COALESCE(estado_documentacion, 'NO_DOCUMENTADO') as estado,
                    COUNT(*) as cantidad
                FROM procesos
                GROUP BY estado_documentacion
            """))
            procesos_stats = dict(result.fetchall())

            # Total procesos
            total_procesos = sum(procesos_stats.values())

    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Inmuebles", total_inmuebles)

    with col2:
        st.metric("Total Procesos", total_procesos)

    with col3:
        documentado = procesos_stats.get("DOCUMENTADO", 0)
        st.metric("Documentados", f"{documentado} ({documentado/total_procesos*100:.1f}%)" if total_procesos > 0 else "0")

    with col4:
        parcial = procesos_stats.get("PARCIALMENTE_DOCUMENTADO", 0)
        st.metric("Parciales", f"{parcial} ({parcial/total_procesos*100:.1f}%)" if total_procesos > 0 else "0")

    # Recent processes
    st.subheader("Procesos Recientes")
    try:
        with SessionLocal() as session:
            result = session.execute(text("""
                SELECT p.id, p.nombre, p.fecha_inicio, p.estado_documentacion,
                       i.nombre as inmueble_nombre
                FROM procesos p
                JOIN inmuebles i ON p.inmueble_id = i.id
                ORDER BY p.fecha_inicio DESC
                LIMIT 10
            """))
            recent_processes = result.fetchall()

            if recent_processes:
                for proc in recent_processes:
                    status_icon = get_status_icon(proc.estado_documentacion or "NO_DOCUMENTADO")

                    st.markdown(f"""
                    <div class="timeline-item">
                        <strong>{status_icon} {proc.nombre}</strong><br>
                        <small>Inmueble: {proc.inmueble_nombre} | Fecha: {proc.fecha_inicio.strftime('%d/%m/%Y') if proc.fecha_inicio else 'N/A'}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay procesos registrados aún.")

    except Exception as e:
        st.error(f"Error cargando procesos recientes: {e}")

def show_inmuebles():
    st.header("🏠 Gestión de Inmuebles")

    # Search and filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Buscar inmueble:", placeholder="Nombre, dirección...")
    with col2:
        tipo_filter = st.selectbox("Tipo:", ["Todos", "Iglesia", "Monasterio", "Ermita"])

    # Get inmuebles
    try:
        with SessionLocal() as session:
            query = """
                SELECT id, nombre, direccion, tipo_inmueble,
                       estado_conservacion, propietario_actual
                FROM inmuebles
                WHERE 1=1
            """
            params = {}

            if search:
                query += " AND (nombre ILIKE :search OR direccion ILIKE :search)"
                params["search"] = f"%{search}%"

            if tipo_filter != "Todos":
                query += " AND tipo_inmueble = :tipo"
                params["tipo"] = tipo_filter

            query += " ORDER BY nombre LIMIT 50"

            result = session.execute(text(query), params)
            inmuebles = result.fetchall()

            if inmuebles:
                # Display as cards
                for inm in inmuebles:
                    with st.expander(f"🏛️ {inm.nombre}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Dirección:** {inm.direccion or 'N/A'}")
                            st.write(f"**Tipo:** {inm.tipo_inmueble or 'N/A'}")
                        with col2:
                            st.write(f"**Estado:** {inm.estado_conservacion or 'N/A'}")
                            st.write(f"**Propietario:** {inm.propietario_actual or 'N/A'}")

                        if st.button(f"Ver procesos de {inm.nombre}", key=f"proc_{inm.id}"):
                            st.session_state.selected_inmueble = inm.id
                            st.rerun()
            else:
                st.info("No se encontraron inmuebles.")

    except Exception as e:
        st.error(f"Error cargando inmuebles: {e}")

def show_procesos():
    st.header("📋 Gestión de Procesos")

    # Check if inmueble selected
    if "selected_inmueble" not in st.session_state:
        st.warning("Selecciona un inmueble desde la vista de Inmuebles para ver sus procesos.")
        return

    inmueble_id = st.session_state.selected_inmueble

    # Get inmueble info
    try:
        with SessionLocal() as session:
            result = session.execute(text("SELECT nombre FROM inmuebles WHERE id = :id"), {"id": inmueble_id})
            inmueble = result.fetchone()
            if inmueble:
                st.subheader(f"Procesos de: {inmueble.nombre}")

                # Timeline
                result = session.execute(text("""
                    SELECT id, nombre, fecha_inicio, estado_documentacion, descripcion
                    FROM procesos
                    WHERE inmueble_id = :inmueble_id
                    ORDER BY fecha_inicio DESC
                """), {"inmueble_id": inmueble_id})

                procesos = result.fetchall()

                if procesos:
                    for proc in procesos:
                        status_icon = get_status_icon(proc.estado_documentacion or "NO_DOCUMENTADO")

                        st.markdown(f"""
                        <div class="timeline-item">
                            <strong>{status_icon} {proc.nombre}</strong><br>
                            <small>Fecha: {proc.fecha_inicio.strftime('%d/%m/%Y') if proc.fecha_inicio else 'N/A'}</small><br>
                            <small>{proc.descripcion or 'Sin descripción'}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Este inmueble no tiene procesos registrados.")

                # New process button
                if st.button("➕ Nuevo Proceso"):
                    st.session_state.show_new_process = True

                if st.session_state.get("show_new_process", False):
                    show_new_process_form(inmueble_id)

    except Exception as e:
        st.error(f"Error cargando procesos: {e}")

def show_new_process_form(inmueble_id):
    st.subheader("Nuevo Proceso")

    with st.form("new_process_form"):
        tipo_proceso = st.selectbox(
            "Tipo de Proceso",
            ["INMATRICULACION", "VENTA", "CESION", "DECLARACION_BIC", "REHABILITACION"]
        )

        fecha_inicio = st.date_input("Fecha de Inicio")
        descripcion = st.text_area("Descripción")

        # Documentos
        st.subheader("Documentos Característicos")
        docs = []

        if tipo_proceso == "INMATRICULACION":
            docs = ["Título de Propiedad", "Nota Simple Registral", "Certificado Catastral"]

        # Simple document status
        doc_status = {}
        for doc in docs:
            doc_status[doc] = st.radio(
                f"{doc}:",
                ["Adjuntar", "Marcar como no disponible"],
                key=f"doc_{doc}"
            )

        submitted = st.form_submit_button("Guardar Proceso")

        if submitted:
            # Here we would save to database
            st.success("Proceso guardado exitosamente (simulado)")
            st.session_state.show_new_process = False
            st.rerun()

def show_configuracion():
    st.header("⚙️ Configuración")
    st.info("Funcionalidad de configuración próximamente disponible.")

if __name__ == "__main__":
    main()</content>
