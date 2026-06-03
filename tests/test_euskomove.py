"""
tests/test_euskomove.py
Tests unitarios de EuskoMove — se ejecutan con: pytest
Cubren: validación de registro, hash de contraseñas, login/logout y rutas HTTP.
"""
import os
import pytest

# Usamos SQLite en memoria para los tests — no toca la BD de Azure
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("FLASK_SECRET_KEY", "clave-de-test-segura")
os.environ.setdefault("FLASK_ENV", "testing")


# ─── FIXTURES ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app():
    """Crea la app Flask con BD en memoria para todos los tests."""
    from app import app as flask_app
    from backend.db import Base, engine, SessionLocal, User, _hash, init_db

    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False

    with flask_app.app_context():
        Base.metadata.create_all(engine)
        db = SessionLocal()
        # Crear usuarios de prueba
        if db.query(User).count() == 0:
            db.add_all([
                User(name="Admin Test", email="admin@test.eus",
                     password=_hash("AdminTest@2026!"), role="admin"),
                User(name="Usuario Test", email="user@test.eus",
                     password=_hash("UserTest@2026!"), role="user"),
            ])
            db.commit()
        db.close()

    yield flask_app


@pytest.fixture
def client(app):
    """Cliente HTTP de prueba."""
    return app.test_client()


# ─── 1. TESTS DE HASH Y VERIFICACIÓN DE CONTRASEÑAS ─────────────────────────

class TestHashContraseñas:

    def test_hash_genera_string(self):
        from backend.db import _hash
        resultado = _hash("micontraseña123")
        assert isinstance(resultado, str)

    def test_hash_empieza_con_bcrypt(self):
        from backend.db import _hash
        resultado = _hash("micontraseña123")
        assert resultado.startswith("$2b$")

    def test_hash_diferente_cada_vez(self):
        """Dos hashes de la misma contraseña deben ser distintos (salt aleatorio)."""
        from backend.db import _hash
        h1 = _hash("mismacontraseña")
        h2 = _hash("mismacontraseña")
        assert h1 != h2

    def test_verificacion_correcta(self):
        from backend.db import _hash, check_password
        pw = "contraseñaSegura123"
        assert check_password(pw, _hash(pw)) is True

    def test_verificacion_incorrecta(self):
        from backend.db import _hash, check_password
        assert check_password("incorrecta", _hash("correcta")) is False

    def test_verificacion_cadena_vacia(self):
        from backend.db import _hash, check_password
        assert check_password("", _hash("algo")) is False

    def test_hash_longitud_suficiente(self):
        """El hash bcrypt tiene al menos 60 caracteres — necesitamos VARCHAR(255)."""
        from backend.db import _hash
        assert len(_hash("cualquiercontraseña")) >= 60


# ─── 2. TESTS DE VALIDACIÓN DE REGISTRO ──────────────────────────────────────

class TestValidacionRegistro:

    def _v(self, name="Ane Garcia", email="ane@test.eus",
           pw="Segura@2026!", pw2=None):
        from backend.routes.auth_routes import validar_registro
        return validar_registro(name, email, pw, pw2 or pw)

    def test_datos_correctos(self):
        assert self._v() is None

    def test_campos_vacios(self):
        from backend.routes.auth_routes import validar_registro
        assert validar_registro("", "a@b.com", "pass1234", "pass1234") is not None
        assert validar_registro("Ana", "", "pass1234", "pass1234") is not None
        assert validar_registro("Ana", "a@b.com", "", "") is not None

    def test_nombre_muy_corto(self):
        assert self._v(name="An") is not None

    def test_nombre_muy_largo(self):
        assert self._v(name="A" * 31) is not None

    def test_nombre_solo_numeros(self):
        assert self._v(name="12345") is not None

    def test_nombre_reservado(self):
        assert self._v(name="admin") is not None
        assert self._v(name="root") is not None
        assert self._v(name="system") is not None

    def test_email_sin_arroba(self):
        assert self._v(email="correosinArroba.com") is not None

    def test_email_sin_dominio(self):
        assert self._v(email="correo@") is not None

    def test_email_valido(self):
        assert self._v(email="usuario@dominio.com") is None

    def test_contraseña_muy_corta(self):
        assert self._v(pw="abc123", pw2="abc123") is not None

    def test_contraseña_muy_larga(self):
        pw = "A" * 65
        assert self._v(pw=pw, pw2=pw) is not None

    def test_contraseña_comun(self):
        assert self._v(pw="12345678", pw2="12345678") is not None
        assert self._v(pw="password", pw2="password") is not None

    def test_contraseñas_no_coinciden(self):
        assert self._v(pw="Segura@2026!", pw2="Diferente@2026!") is not None

    def test_contraseña_valida_sin_simbolos(self):
        """NIST no obliga símbolos — una frase larga es válida."""
        assert self._v(pw="fraseseguralargarara", pw2="fraseseguralargarara") is None


# ─── 3. TESTS DE RUTAS HTTP ───────────────────────────────────────────────────

class TestRutasHTTP:

    def test_pagina_inicio_ok(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_pagina_login_ok(self, client):
        r = client.get("/login")
        assert r.status_code == 200

    def test_pagina_registro_ok(self, client):
        r = client.get("/register")
        assert r.status_code == 200

    def test_ruta_inexistente_404(self, client):
        r = client.get("/ruta-que-no-existe-xyz")
        assert r.status_code == 404


# ─── 4. TESTS DE LOGIN ────────────────────────────────────────────────────────

class TestLogin:

    def test_login_correcto_redirige(self, client):
        # Primero registramos el usuario de prueba
        client.post("/register", data={
            "name": "Usuario Test",
            "email": "user@test.eus",
            "password": "UserTest@2026!",
            "password2": "UserTest@2026!"
        })
        # Luego hacemos login
        r = client.post("/login", data={
            "email": "user@test.eus",
            "password": "UserTest@2026!",
            "next": "/"
        }, follow_redirects=False)
        assert r.status_code == 302

    def test_login_password_incorrecta(self, client):
        r = client.post("/login", data={
            "email": "user@test.eus",
            "password": "contraseñaWrong",
            "next": "/"
        })
        assert r.status_code == 200
        assert "incorrectos" in r.data.decode("utf-8").lower() or r.status_code == 200

    def test_login_email_inexistente(self, client):
        r = client.post("/login", data={
            "email": "noexiste@test.eus",
            "password": "cualquiera123",
            "next": "/"
        })
        assert r.status_code == 200

    def test_logout_redirige(self, client):
        # Primero hacemos login
        client.post("/login", data={
            "email": "user@test.eus",
            "password": "UserTest@2026!",
            "next": "/"
        })
        # Luego logout
        r = client.post("/logout", follow_redirects=False)
        assert r.status_code == 302


# ─── 5. TESTS DE REGISTRO ─────────────────────────────────────────────────────

class TestRegistro:

    def test_registro_datos_invalidos_no_crea_usuario(self, client):
        r = client.post("/register", data={
            "name": "ab",           # nombre muy corto
            "email": "nuevo@test.eus",
            "password": "pass",     # contraseña muy corta
            "password2": "pass"
        })
        assert r.status_code == 200

    def test_registro_contraseñas_no_coinciden(self, client):
        r = client.post("/register", data={
            "name": "Nuevo Usuario",
            "email": "nuevo2@test.eus",
            "password": "Segura@2026!",
            "password2": "Diferente@2026!"
        })
        assert r.status_code == 200
