import reflex as rx
import requests

# 1. ESTADO: Lógica de datos
class State(rx.State):
    origen: str = ""
    destino: str = ""
    horarios: list[dict] = []
    loading: bool = False

    def buscar_viajes(self):
        self.loading = True
        try:
            # Asegúrate de que tu backend esté corriendo en el puerto 8000
            res = requests.get(
                "http://localhost:8000/api/horarios/", 
                params={"origen": self.origen, "destino": self.destino}
            )
            if res.status_code == 200:
                self.horarios = res.json()
        except Exception as e:
            print(f"Error conectando al backend: {e}")
        self.loading = False

# 2. INTERFAZ: Lo que se ve
def index() -> rx.Component:
    return rx.box(
        # NAVBAR corregido
        rx.box(
            rx.box("Eusko", rx.span("Move"), class_name="nav-logo"),
            rx.link("Horarios", href="/", class_name="nav-link"),
            rx.link("Entrar", href="/", class_name="nav-btn"),
            tag="nav",
            class_name="nav",
        ),

        # HERO SECTION corregido
        rx.box(
            rx.box(class_name="hero-glow"),
            rx.heading("Viaja por Euskadi con Python", class_name="hero-title"),
            rx.text("Sin una sola línea de JavaScript.", class_name="hero-p"),
            tag="section",
            class_name="hero",
        ),

        # BUSCADOR
        rx.box(
            rx.input(placeholder="Origen", on_change=State.set_origen, class_name="form-group"),
            rx.input(placeholder="Destino", on_change=State.set_destino, class_name="form-group"),
            rx.button(
                "Buscar", 
                on_click=State.buscar_viajes, 
                is_loading=State.loading,
                class_name="btn-primary"
            ),
            class_name="search-box",
        ),

        # TABLA DE RESULTADOS
        rx.table(
            rx.thead(
                rx.tr(
                    rx.th("Línea"), 
                    rx.th("Trayecto"), 
                    rx.th("Salida")
                )
            ),
            rx.tbody(
                rx.foreach(
                    State.horarios,
                    lambda h: rx.tr(
                        rx.td(rx.badge(h["linea"], class_name="badge-orange")),
                        rx.td(f"{h['origen']} → {h['destino']}"),
                        rx.td(h["hora_salida"]),
                    )
                )
            ),
            class_name="route-table",
        ),
        class_name="main-container"
    )

# 3. CONFIGURACIÓN DE LA APP
app = rx.App(
    stylesheets=[
        "/style.css",  # Carga tu archivo de la carpeta assets/
    ],
)
app.add_page(index)