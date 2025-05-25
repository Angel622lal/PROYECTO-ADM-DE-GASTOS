# Gestor de Gastos Familiares

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)

Aplicación de escritorio en Python para el registro y control integral de ingresos, egresos y ahorros mensuales, con gestión de usuarios, categorías con límites y reportes dinámicos.

---

## 📋 Descripción

Este proyecto ofrece una solución para que usuarios individuales o familias puedan:

* **Registrar** y **controlar** gastos e ingresos por categoría.
* **Visualizar** el estado de ahorro en tiempo real, con alertas de excedentes y posibles adeudos.
* **Configurar** límites por categoría para un presupuesto más estricto.
* **Generar** reportes detallados y realizar cortes mensuales de manera sencilla.

La aplicación se divide en:

1. **Backend** (`BackendGastos.py`): lógica de negocio y persistencia en archivos JSON.
2. **Frontend** (`FrontedGasto.py`): interfaz gráfica con Tkinter y ttk.

---

## 🚀 Características principales

* **Gestión de Usuarios**: registro y login con almacenamiento seguro en `usuarios.json`.
* **Categorías y Límites**: creación, edición y persistencia en `categorias.json`.
* **Ingresos/Egresos**: registro en tiempo real con validación de límites y alertas (sobre límite y ahorro insuficiente).
* **Ahorro**: cálculo automático del saldo, alertas de posible adeudo y corte mensual.
* **Búsqueda avanzada**: filtros por categoría, tipo, rangos de importe y fechas.
* **Reportes**: generación de reportes por periodo (formato YYYYMM) con resumen por categoría y ahorro final.

---

## 🎯 Requisitos

* **Python 3.13**
* Paquetes:

  * `python-dateutil`
  * `Pillow`

Instálalos con:

```bash
pip install python-dateutil Pillow
```

---

## ▶️ Instalación y uso

1. **Clonar el repositorio**:

   ```bash
   ```

git clone [https://github.com/Angel622lal/PROYECTO-ADM-DE-GASTOS.git](https://github.com/Angel622lal/PROYECTO-ADM-DE-GASTOS.git)
cd PROYECTO-ADM-DE-GASTOS

````
2. **(Opcional) Crear y activar entorno virtual**:
   ```bash
python -m venv venv
# Windows
env\Scripts\activate
# macOS/Linux
source venv/bin/activate
````

3. **Instalar dependencias**:

   ```bash
   ```

pip install -r requirements.txt  # si tienes un archivo

# o instala manualmente

pip install python-dateutil Pillow

````
4. **Ejecutar la aplicación**:
   ```bash
python FrontedGasto.py
````

5. **Generar ejecutable** (opcional):

   ```bash
   ```

python -m PyInstaller --onefile FrontedGasto.py

```

---

## 🔧 Configuración

- **Archivos JSON**:
  - `usuarios.json`: almacena usuarios.
  - `categorias.json`: categorías y límites.
  - `ingegr.json`: registros de ingresos/egresos.
  - `ahorro.json`: historial de ahorros.

- **Rutas de imágenes**:
  - Icono `Icogasto.ico` y fondo `Portadagestion.jpeg` deben estar en la carpeta del proyecto o ajustar rutas en el código.

---

## 🛠️ Estructura del proyecto

```

PROYECTO-ADM-DE-GASTOS/
├── BackendGastos.py      # Lógica de negocio y JSON
├── FrontedGasto.py       # Interfaz gráfica
├── usuarios.json         # Datos de usuarios
├── categorias.json       # Límites y descripciones
├── ingegr.json           # Entradas y salidas
├── ahorro.json           # Ahorro mensual
├── Icogasto.ico          # Icono de la app
├── Portadagestion.jpeg   # Imagen de fondo
├── requirements.txt      # Dependencias opcionales
└── README.md             # Documentación del proyecto

```

---

## 🛠️ Ejemplo de uso

1. Iniciar sesión con usuario preexistente.
2. Crear categorías con límites (Egreso/Ingreso).
3. Registrar ingresos y egresos; ver alertas en caso de exceso.
4. Revisar ahorro actual y sugerencia basada en mes anterior.
5. Realizar corte de mes para nuevo periodo.
6. Utilizar pestañas de búsqueda y reportes para análisis detallado.

---

## 🤝 Contribuciones

¡Bienvenidas! Para contribuir:
1. Realiza un **fork**.
2. Crea una rama: `git checkout -b feature/nombre`.
3. Realiza **commits** claros.
4. Envía un **pull request**.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Revisa `LICENSE` para más detalles.

---

## 👤 Autor

Desarrollado por: **Angel Camacho Balderas**

---

*¡Gracias por utilizar el Gestor de Gastos Familiares!*

```
