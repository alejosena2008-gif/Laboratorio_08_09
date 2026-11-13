# ClassroomHub — Laboratorio 9: Formularios y CRUD con Django (Vistas, ModelForm y Permisos)

**ClassroomHub** integra en este laboratorio un flujo completo y robusto de **CRUD (creación, consulta de detalle, actualización y eliminación) de recursos** desde la interfaz web, utilizando `ResourceForm` (`ModelForm`), vistas genéricas basadas en clases (`DetailView`, `CreateView`, `UpdateView`, `DeleteView`), `LoginRequiredMixin` y `PermissionRequiredMixin` para proteger cada operación según su permiso específico.

## Requisitos y compatibilidad

- **Python:** 3.10+ (probado con Python 3.14)
- **Django:** 5.1+ / 6.1+
- **Motor de Base de Datos:**
  - **SQLite:** Listo para usar de inmediato (`db.sqlite3`), sin configuración adicional.
  - **MariaDB / MySQL:** Compatible mediante variables en `.env` y soporte `pymysql` / `mysqlclient`.
- **Dependencias:** `asgiref`, `Django`, `pymysql`, `python-dotenv`, `sqlparse`

## Matriz de permisos y rutas

| Operación / Ruta | Anónimo | Cuenta común (`reader_demo`) | `Catalog reviewers` (`reviewer_demo`) | `Catalog editors` (`editor_demo`) |
|---|---|---|---|---|
| `GET /resources/` y `GET /resources/<pk>/` | Sí | Sí | Sí | Sí |
| `GET /dashboard/` | Redirige a login | Sí | Sí | Sí |
| `GET /resources/review/` (`pages.view_resource`) | Redirige a login | `403` | Sí | Sí |
| `GET/POST /resources/new/` (`pages.add_resource`) | Redirige a login | `403` | `403` | Sí |
| `GET/POST /resources/<pk>/edit/` (`pages.change_resource`) | Redirige a login | `403` | `403` | Sí |
| `GET/POST /resources/<pk>/delete/` (`pages.delete_resource`) | Redirige a login | `403` | `403` | Sí |

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
   *Crea automáticamente los grupos `Catalog reviewers` y `Catalog editors`, categorías y los siguientes usuarios de prueba:*
   - **Administrador:** `admin` / `AdminPassword123!` (Superusuario)
   - **Editor de catálogo:** `editor_demo` / `EditorPassword123!` (Miembro de `Catalog editors` — permisos CRUD completos)
   - **Revisor de catálogo:** `reviewer_demo` / `ReviewerPassword123!` (Miembro de `Catalog reviewers` — permiso de vista)
   - **Usuario estándar:** `reader_demo` / `ReaderPassword123!` (Sin permisos de edición)

4. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

5. **Ejecutar pruebas automatizadas:**
   ```bash
   python manage.py test pages
   ```
   *Resultado esperado:* **Ran 58 tests — OK**.
