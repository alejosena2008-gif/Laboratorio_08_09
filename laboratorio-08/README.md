# ClassroomHub — Laboratorio 8: Autenticación, sesiones, grupos y permisos en Django

**ClassroomHub** amplía el catálogo persistente del Laboratorio 7 incorporando **registro público de cuentas sin privilegios (`UserCreationForm`), inicio y cierre de sesión seguros (`LoginView` y `LogoutView` por POST con CSRF), un panel privado con contador de sesión (`/dashboard/`) y una vista de revisión autorizada por permisos (`/resources/review/` para el grupo `Catalog reviewers`)**.

## Requisitos y compatibilidad

- **Python:** 3.10+ (probado con Python 3.14)
- **Django:** 5.1+ / 6.1+
- **Motor de Base de Datos:**
  - **SQLite:** Listo para usar de inmediato (`db.sqlite3`), sin configuración adicional.
  - **MariaDB / MySQL:** Compatible mediante variables en `.env` y soporte `pymysql` / `mysqlclient`.
- **Dependencias:** `asgiref`, `Django`, `pymysql`, `python-dotenv`, `sqlparse`

## Rutas de la aplicación

| Ruta | Método | Nombre | Control de acceso | Descripción |
|---|---|---|---|---|
| `/` | `GET` | `pages:home` | Público | Página de inicio |
| `/resources/` | `GET` | `pages:resources` | Público | Catálogo público de recursos |
| `/about/` | `GET` | `pages:about` | Público | Información del proyecto |
| `/accounts/signup/` | `GET`, `POST` | `pages:signup` | Público (redirige si ya hay sesión) | Registro de cuentas comunes sin privilegios |
| `/accounts/login/` | `GET`, `POST` | `pages:login` | Público | Inicio de sesión (`LoginView`) |
| `/accounts/logout/` | `POST` | `pages:logout` | Autenticado / CSRF | Cierre de sesión mediante `POST` (`GET` devuelve `405`) |
| `/dashboard/` | `GET` | `pages:dashboard` | `@login_required` | Panel privado con contador de visitas en `request.session` |
| `/resources/review/` | `GET` | `pages:resource-review` | `@login_required` + `pages.view_resource` | Vista de revisión reservada al grupo `Catalog reviewers` (`403` sin permiso) |

## Puesta en marcha rápida

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

3. **Cargar datos de demostración y roles automáticamente:**
   ```bash
   python manage.py setup_demo_data
   ```
   *Crea automáticamente el grupo `Catalog reviewers`, el permiso `pages.view_resource`, categorías y los siguientes usuarios:*
   - **Administrador:** `admin` / `AdminPassword123!` (Superusuario)
   - **Revisor de catálogo:** `reviewer_demo` / `ReviewerPassword123!` (Acceso a `/resources/review/`)
   - **Usuario estándar:** `reader_demo` / `ReaderPassword123!` (Acceso a `/dashboard/`)

4. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

5. **Ejecutar pruebas automatizadas:**
   ```bash
   python manage.py test pages
   ```
   *Resultado esperado:* **Ran 28 tests — OK**.
