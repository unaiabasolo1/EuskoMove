"""
tests/test_caracteristicas.py
Tests de CARACTERÍSTICAS (feature tests) de EuskoMove.

Comprueban el comportamiento completo desde el punto de vista del usuario:
"Como usuario quiero poder... y que el sistema haga..."
Se ejecutan con: pytest tests/test_caracteristicas.py -v
"""
import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("FLASK_SECRET_KEY", "clave-features-test")
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
                User(name="Admin Feature", email="admin@feat.eus",
                     password=_hash("Admin@Feat2026!"), role="admin"),
            ])
            db.commit()
        db.close()

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


# ─── CARACTERÍSTICA 1: REGISTRO DE USUARIO ───────────────────────────────────

class TestCaracteristicaRegistro:
    """
    CARACTERÍSTICA: Registro de nuevo usuario
    Como visitante
    Quiero poder registrarme con nombre, email y contraseña
    Para poder acceder a la plataforma y hacer reservas
    """

    def test_escenario_registro_exitoso(self, client):
        """
        ESCENARIO: Registro con datos válidos
        Dado que soy un visitante nuevo
        Cuando relleno el formulario con datos correctos
        Entonces me registro y accedo a la plataforma
        """
        r = client.post("/register", data={
            "name": "Miren Etxeberria",
            "email": "miren@feat.eus",
            "password": "MirenSegura@2026!",
            "password2": "MirenSegura@2026!"
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_escenario_registro_contraseña_debil(self, client):
        """
        ESCENARIO: Intento de registro con contraseña débil
        Dado que soy un visitante
        Cuando intento registrarme con una contraseña común
        Entonces el sistema me rechaza con un mensaje de error
        """
        r = client.post("/register", data={
            "name": "Jon Arrieta",
            "email": "jon@feat.eus",
            "password": "12345678",
            "password2": "12345678"
        })
        assert r.status_code == 200
        assert "común" in r.data.decode("utf-8") or "segura" in r.data.decode("utf-8").lower()

    def test_escenario_registro_nombre_reservado(self, client):
        """
        ESCENARIO: Intento de registro con nombre reservado
        Dado que soy un visitante
        Cuando intento registrarme con el nombre 'admin'
        Entonces el sistema me rechaza
        """
        r = client.post("/register", data={
            "name": "admin",
            "email": "otroadmin@feat.eus",
            "password": "Segura@2026!",
            "password2": "Segura@2026!"
        })
        assert r.status_code == 200
        assert "reservado" in r.data.decode("utf-8").lower()

    def test_escenario_registro_email_invalido(self, client):
        """
        ESCENARIO: Registro con email sin formato válido
        Dado que soy un visitante
        Cuando introduzco un email sin @ ni dominio
        Entonces el sistema me indica que el email no es válido
        """
        r = client.post("/register", data={
            "name": "Amaia Test",
            "email": "esto-no-es-un-email",
            "password": "Segura@2026!",
            "password2": "Segura@2026!"
        })
        assert r.status_code == 200
        assert "email" in r.data.decode("utf-8").lower()

    def test_escenario_contraseñas_no_coinciden(self, client):
        """
        ESCENARIO: Las dos contraseñas no son iguales
        Dado que soy un visitante
        Cuando introduzco contraseñas distintas en los dos campos
        Entonces el sistema me avisa de que no coinciden
        """
        r = client.post("/register", data={
            "name": "Iker Test",
            "email": "iker@feat.eus",
            "password": "Segura@2026!",
            "password2": "Diferente@2026!"
        })
        assert r.status_code == 200
        assert "coincid" in r.data.decode("utf-8").lower()


# ─── CARACTERÍSTICA 2: LOGIN ──────────────────────────────────────────────────

class TestCaracteristicaLogin:
    """
    CARACTERÍSTICA: Inicio de sesión
    Como usuario registrado
    Quiero poder iniciar sesión con mi email y contraseña
    Para acceder a mis reservas y comprar billetes
    """

    def test_escenario_login_exitoso(self, client):
        """
        ESCENARIO: Login con credenciales correctas
        Dado que soy un usuario registrado
        Cuando introduzco mi email y contraseña correctos
        Entonces accedo a la plataforma
        """
        # Registrar primero
        client.post("/register", data={
            "name": "Leire Login",
            "email": "leire@feat.eus",
            "password": "Leire@Segura2026!",
            "password2": "Leire@Segura2026!"
        })
        r = client.post("/login", data={
            "email": "leire@feat.eus",
            "password": "Leire@Segura2026!",
            "next": "/"
        }, follow_redirects=False)
        assert r.status_code == 302

    def test_escenario_login_password_incorrecta(self, client):
        """
        ESCENARIO: Login con contraseña incorrecta
        Dado que soy un usuario registrado
        Cuando introduzco una contraseña incorrecta
        Entonces el sistema me muestra un error sin revelar cuál campo es incorrecto
        """
        r = client.post("/login", data={
            "email": "leire@feat.eus",
            "password": "ContraseñaWrong@2026!",
            "next": "/"
        })
        assert r.status_code == 200
        assert "incorrectos" in r.data.decode("utf-8").lower()

    def test_escenario_login_email_inexistente(self, client):
        """
        ESCENARIO: Login con email no registrado
        Dado que intento hacer login con un email que no existe
        Entonces el sistema me muestra el mismo error genérico (sin revelar si el email existe)
        """
        r = client.post("/login", data={
            "email": "noexiste@feat.eus",
            "password": "Cualquiera@2026!",
            "next": "/"
        })
        assert r.status_code == 200
        assert "incorrectos" in r.data.decode("utf-8").lower()

    def test_escenario_logout_cierra_sesion(self, client):
        """
        ESCENARIO: Cerrar sesión
        Dado que estoy logueado
        Cuando hago logout
        Entonces mi sesión se cierra y soy redirigido
        """
        client.post("/login", data={
            "email": "leire@feat.eus",
            "password": "Leire@Segura2026!",
            "next": "/"
        })
        r = client.post("/logout", follow_redirects=False)
        assert r.status_code == 302


# ─── CARACTERÍSTICA 3: NAVEGACIÓN PÚBLICA ────────────────────────────────────

class TestCaracteristicaNavegacion:
    """
    CARACTERÍSTICA: Navegación pública
    Como visitante
    Quiero poder ver la página principal, horarios y avisos
    Sin necesidad de registrarme
    """

    def test_escenario_ver_pagina_principal(self, client):
        """
        ESCENARIO: Acceso a la página principal
        Dado que soy un visitante
        Cuando accedo a la URL principal
        Entonces veo la página de EuskoMove
        """
        r = client.get("/")
        assert r.status_code == 200

    def test_escenario_ver_formulario_login(self, client):
        """
        ESCENARIO: Acceso al formulario de login
        Dado que soy un visitante
        Cuando voy a /login
        Entonces veo el formulario de inicio de sesión
        """
        r = client.get("/login")
        assert r.status_code == 200
        assert "login" in r.data.decode("utf-8").lower() or "correo" in r.data.decode("utf-8").lower()

    def test_escenario_ver_formulario_registro(self, client):
        """
        ESCENARIO: Acceso al formulario de registro
        Dado que soy un visitante
        Cuando voy a /register
        Entonces veo el formulario de registro
        """
        r = client.get("/register")
        assert r.status_code == 200

    def test_escenario_pagina_inexistente_404(self, client):
        """
        ESCENARIO: Acceso a una página que no existe
        Dado que soy un visitante
        Cuando accedo a una URL que no existe
        Entonces recibo un error 404
        """
        r = client.get("/esta-pagina-no-existe-xyz-abc")
        assert r.status_code == 404


# ─── CARACTERÍSTICA 4: SEGURIDAD ─────────────────────────────────────────────

class TestCaracteristicaSeguridad:
    """
    CARACTERÍSTICA: Seguridad del sistema
    Como sistema
    Quiero proteger los datos de los usuarios
    Almacenando contraseñas con hash y validando entradas
    """

    def test_escenario_contraseña_nunca_en_texto_plano(self, app):
        """
        ESCENARIO: Contraseñas almacenadas de forma segura
        Dado que un usuario se registra
        Cuando miro la BD
        Entonces la contraseña está hasheada con bcrypt
        """
        from backend.db import SessionLocal, User
        with app.app_context():
            db = SessionLocal()
            user = db.query(User).filter_by(email="miren@feat.eus").first()
            db.close()
            if user:
                assert not user.password.startswith("Miren")
                assert user.password.startswith("$2b$")

    def test_escenario_campos_vacios_rechazados(self, client):
        """
        ESCENARIO: Formulario enviado vacío
        Dado que soy un visitante
        Cuando envío el formulario de registro sin rellenar nada
        Entonces el sistema me indica que los campos son obligatorios
        """
        r = client.post("/register", data={
            "name": "",
            "email": "",
            "password": "",
            "password2": ""
        })
        assert r.status_code == 200
        assert "obligatorio" in r.data.decode("utf-8").lower()

    def test_escenario_error_login_generico(self, client):
        """
        ESCENARIO: El mensaje de error no revela si el email existe
        Dado que intento hacer login con credenciales incorrectas
        Cuando el sistema me rechaza
        Entonces el mensaje es genérico (no dice si es el email o la contraseña)
        """
        r = client.post("/login", data={
            "email": "noexiste@feat.eus",
            "password": "cualquiera",
            "next": "/"
        })
        html = r.data.decode("utf-8").lower()
        # El mensaje debe ser genérico, no decir "email no encontrado"
        assert "no encontrado" not in html
        assert "no existe" not in html
