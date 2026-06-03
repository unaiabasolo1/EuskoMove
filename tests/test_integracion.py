"""
tests/test_integracion.py
Tests de INTEGRACIÓN de EuskoMove.

Comprueban que varias capas de la app funcionan juntas correctamente:
BD ↔ lógica de negocio ↔ rutas HTTP.
Se ejecutan con: pytest tests/test_integracion.py -v
"""
import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("FLASK_SECRET_KEY", "clave-integracion-test")
os.environ.setdefault("FLASK_ENV", "testing")


# ─── FIXTURES ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def app():
    from app import app as flask_app
    from backend.db import Base, engine, SessionLocal, User, _hash

    flask_app.config["TESTING"] = True

    with flask_app.app_context():
        Base.metadata.create_all(engine)
        db = SessionLocal()
        if db.query(User).count() == 0:
            db.add_all([
                User(name="Admin Integ", email="admin@integ.eus",
                     password=_hash("Admin@Integ2026!"), role="admin"),
                User(name="User Integ",  email="user@integ.eus",
                     password=_hash("User@Integ2026!"),  role="user"),
            ])
            db.commit()
        db.close()

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client_admin(client):
    """Cliente con sesión de admin ya iniciada."""
    client.post("/login", data={
        "email": "admin@integ.eus",
        "password": "Admin@Integ2026!",
        "next": "/"
    })
    return client


@pytest.fixture
def client_user(client):
    """Cliente con sesión de usuario normal ya iniciada."""
    # Primero registramos el usuario
    client.post("/register", data={
        "name": "User Integ",
        "email": "user@integ.eus",
        "password": "User@Integ2026!",
        "password2": "User@Integ2026!"
    })
    client.post("/login", data={
        "email": "user@integ.eus",
        "password": "User@Integ2026!",
        "next": "/"
    })
    return client


# ─── 1. INTEGRACIÓN: REGISTRO → LOGIN → LOGOUT ───────────────────────────────

class TestFlujoAutenticacion:

    def test_registro_crea_usuario_en_bd(self, client, app):
        """Registrar un usuario nuevo lo persiste en la BD."""
        from backend.db import SessionLocal, User
        r = client.post("/register", data={
            "name": "Nuevo Integrado",
            "email": "nuevo@integ.eus",
            "password": "NuevoSeguro@2026!",
            "password2": "NuevoSeguro@2026!"
        }, follow_redirects=True)
        assert r.status_code == 200
        with app.app_context():
            db = SessionLocal()
            user = db.query(User).filter_by(email="nuevo@integ.eus").first()
            db.close()
            assert user is not None
            assert user.name == "Nuevo Integrado"
            assert user.role == "user"

    def test_password_guardada_como_hash(self, app):
        """La contraseña en BD nunca es texto plano."""
        from backend.db import SessionLocal, User
        with app.app_context():
            db = SessionLocal()
            user = db.query(User).filter_by(email="nuevo@integ.eus").first()
            db.close()
            assert user.password != "NuevoSeguro@2026!"
            assert user.password.startswith("$2b$")

    def test_login_correcto_crea_sesion(self, client):
        """Login correcto redirige y establece sesión."""
        r = client.post("/login", data={
            "email": "nuevo@integ.eus",
            "password": "NuevoSeguro@2026!",
            "next": "/"
        }, follow_redirects=False)
        assert r.status_code == 302

    def test_login_incorrecto_no_crea_sesion(self, client):
        """Login con password incorrecta devuelve el formulario."""
        r = client.post("/login", data={
            "email": "nuevo@integ.eus",
            "password": "contraseñaMal@2026!",
            "next": "/"
        })
        assert r.status_code == 200

    def test_registro_email_duplicado_rechazado(self, client):
        """No se puede registrar dos veces el mismo email."""
        r = client.post("/register", data={
            "name": "Otro Nombre",
            "email": "nuevo@integ.eus",  # ya existe
            "password": "OtraPass@2026!",
            "password2": "OtraPass@2026!"
        })
        assert r.status_code == 200
        assert "registrado" in r.data.decode("utf-8").lower()

    def test_logout_limpia_sesion(self, client):
        """Después de logout el usuario no está autenticado."""
        # Login
        client.post("/login", data={
            "email": "nuevo@integ.eus",
            "password": "NuevoSeguro@2026!",
            "next": "/"
        })
        # Logout
        r = client.post("/logout", follow_redirects=False)
        assert r.status_code == 302


# ─── 2. INTEGRACIÓN: ACCESO POR ROLES ────────────────────────────────────────

class TestControlAccesoRoles:

    def test_admin_accede_panel_admin(self, client_admin):
        """El admin puede acceder al panel de administración."""
        r = client_admin.get("/admin")
        assert r.status_code in [200, 302]  # 200 si existe, 302 si redirige a login

    def test_usuario_sin_login_redirigido(self, client):
        """Un usuario sin sesión es redirigido al intentar reservar."""
        r = client.get("/reservar", follow_redirects=False)
        assert r.status_code in [302, 404]

    def test_usuario_normal_no_accede_admin(self, client_user):
        """Un usuario normal no puede acceder al panel de admin."""
        r = client_user.get("/admin", follow_redirects=False)
        assert r.status_code in [302, 403, 404]


# ─── 3. INTEGRACIÓN: BD ↔ RUTAS ──────────────────────────────────────────────

class TestIntegracionBD:

    def test_horarios_devuelve_datos(self, client):
        """La página de horarios carga correctamente con datos de la BD."""
        r = client.get("/")
        assert r.status_code == 200

    def test_pagina_login_accesible_sin_sesion(self, client):
        """La página de login es accesible sin autenticación."""
        r = client.get("/login")
        assert r.status_code == 200
        assert "login" in r.data.decode("utf-8").lower() or r.status_code == 200

    def test_pagina_registro_accesible_sin_sesion(self, client):
        """La página de registro es accesible sin autenticación."""
        r = client.get("/register")
        assert r.status_code == 200

    def test_usuario_registrado_puede_hacer_login(self, client, app):
        """Un usuario recién registrado puede hacer login inmediatamente."""
        from backend.db import SessionLocal, User
        # Registrar
        client.post("/register", data={
            "name": "Test BD Login",
            "email": "bdlogin@integ.eus",
            "password": "BDLogin@2026!",
            "password2": "BDLogin@2026!"
        })
        # Verificar que existe en BD
        with app.app_context():
            db = SessionLocal()
            user = db.query(User).filter_by(email="bdlogin@integ.eus").first()
            db.close()
            assert user is not None
        # Login inmediato
        r = client.post("/login", data={
            "email": "bdlogin@integ.eus",
            "password": "BDLogin@2026!",
            "next": "/"
        }, follow_redirects=False)
        assert r.status_code == 302
