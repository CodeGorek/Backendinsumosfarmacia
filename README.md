# Proyecto 5: Pedidos de Insumos Médicos (B2B)

**Desarrollado por:** Oscar Javier Pérez Salazar  
**Sección:** IEC-N4-C1  
**Año:** 2026  

---

## 📌 Descripción del Proyecto
Plataforma B2B para la gestión de abastecimiento médico. Permite a las Instituciones Médicas realizar órdenes de compra mediante un catálogo web, y a los Gestores de Bodega administrar el inventario y procesar los despachos.

El backend está desarrollado con **Django** y **Django REST Framework (DRF)**, utilizando **Tokens JWT** para la autenticación y **PostgreSQL** como motor de base de datos.

---

## ⚙️ Guía Rápida de Instalación (Entorno Virtual)

Para asegurar que el proyecto se ejecute de manera limpia sin conflictos de versiones, por favor siga estos pasos para crear su propio Entorno Virtual e instalar todas las dependencias (librerías) de golpe:

### 1. Crear el Entorno Virtual
Abra la terminal en la raíz de este proyecto (donde se encuentra este archivo) y ejecute:
```bash
python -m venv venv
```

### 2. Activar el Entorno Virtual
* **En Windows:**
  ```bash
  venv\Scripts\activate
  ```
* **En Mac / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar Todas las Dependencias (¡El comando mágico!)
Una vez activado el entorno (verá un `(venv)` en su terminal), ejecute este comando para instalar automáticamente Django, REST Framework, PostgreSQL drivers y todas las librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos y Ejecutar
Asegúrese de tener PostgreSQL corriendo con la base de datos `farmacia_db` (credenciales en `config/settings.py`), aplique las migraciones y corra el servidor:
```bash
python manage.py migrate
python manage.py runserver
```

---
*Nota Técnica: La carpeta `venv/` original no se subió al repositorio de GitHub de manera intencional mediante `.gitignore` para cumplir con los estándares de desarrollo limpio.*
