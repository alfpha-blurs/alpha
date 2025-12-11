# 📒 **Uxio — App de Notas en Python + Flet (Versión Base)**

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com)



---

## 🧩 **¿Qué es Uxio?**

**Uxio** es el **núcleo oficial** de una aplicación de notas hecha en **Python + Flet**.

Está pensada para:

* Personas que quieren **crear su propia app de notas**
* Usuarios que quieren **estudiar cómo funciona una app con Flet**
* Desarrolladores que necesitan un **proyecto base** listo para extender

Este repo contiene la **versión libre y abierta**, diseñada para ser simple, clara y fácil de modificar.
Más adelante existirá una **versión Pro / Código cerrado**, con muchas más funciones.

---

## 🖥️ **Vista de la Aplicación**

> ⚠️ *Añade tus capturas dentro de los bloques cuando las tengas.*

### 🏠 Pantalla Principal

```
![Home](assets/screenshot_home.png)
```

### 📝 Crear / Editar Nota

```
![Editor](assets/screenshot_editor.png)
```

### ⚙️ Ajustes (Tema, tamaño, radio, preview)

```
![Settings](assets/screenshot_settings.png)
```

---

## 🎨 **Características Principales**

### ✔️ Gestión completa de notas

* Crear notas

* Buscador con animación

* Vista previa al dejar presionado en la parte inferior de la nota

### ✔️ Temas dinámicos integrados

Tu app incluye **5 temas** listos para usar:

* Pro
* Tec
* Pastel
* Elegante
* Golden

Cada uno cambia colores del fondo, acentos, texto y gradientes.

### ✔️ Ajustes personalizables

Desde la pantalla de configuración puedes cambiar:

* Tema visual
* Tamaño de fuente
* Vista previa on/off
* Radio de borde
* Preview markdown en el editor
* Reinicios automáticos para aplicar cambios

### ✔️ Animaciones modernas

* Animaciones de escala
* Transiciones suaves
* Búsqueda emergente
* Aparición del menú lateral

---

## 🧱 **Arquitectura del Proyecto**

La estructura real según tu código es:

```
alpha/
│
├─ contenedores.json   // Datos de notas
├─ settings.json        // Ajustes de la app
├─ main.py              // App completa en Flet
└─ README.md
```

---

## 🧠 **Cómo Funciona Internamente**

### 🎨 Temas

El sistema de temas usa `get_theme_colors()` para definir paletas completas.

### 🧩 Widgets principales

* `GridView` para notas
* `CupertinoPicker` para seleccionar temas, tamaños y radios
* `LinearGradient` para fondos dinámicos
* `Markdown` para preview de notas

### 🗄️ Sistema de datos

* Se guarda todo en JSON
* Manejo seguro si los archivos no existen
* Corrección automática de claves faltantes

---

## 🚀 **Instalación**

### 1️⃣ Instalar Flet

```bash
pip install flet
```

### 2️⃣ Ejecutar la app

```bash
python main.py
```

### 3️⃣ Asegúrate de que existan estos archivos:

* `settings.json` (se crea solo)
* `contenedores.json` (también se crea solo)

---

## 📱 **APK y versión compilada**

Publicaré la versión APK lista para instalar directamente en Android muy pronto.

El enlace aparecerá aquí mismo:

```
📦 [Descargar APK](#)
```

---

## 📘 **Documentación Oficial**

Toda la documentación está aquí:

👉 [**https://alfpha-blurs.github.io/alpha.github.io/**](https://alfpha-blurs.github.io/alpha.github.io/)

Incluye guías para edición, estructura, funciones y estilos.

---

## 🚀 **Roadmap**

**Versión Base (este repo)**

*

**Versión Pro (código cerrado)**

*

---

## 🤝 Contribuciones

Este repositorio está pensado como base educativa.
Puedes contribuir con:

* Correcciones
* Ideas
* Ejemplos
* Pequeñas mejoras

---

## ⭐ Si te gusta Alpha, ¡déjale una estrella!

Una estrella ayuda a que más personas descubran este proyecto ✨
