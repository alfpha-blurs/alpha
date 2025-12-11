# main.py
import flet as ft
import json
import os
import random
from datetime import date

DATA_FILE = "contenedores.json"
DATA_SETTINGS = "settings.json"

# -------------------------
# UTILIDADES DE CONFIG
# -------------------------
def load_settings():
    """Carga settings desde archivo; devuelve valores por defecto si no existe o está corrupto."""
    defaults = {
        "theme": "Pro",
        "font_size": "2",
        "preview": True,
        "bradius": 20.0,
        "pw": False
    }
    if not os.path.exists(DATA_SETTINGS):
        return defaults
    try:
        with open(DATA_SETTINGS, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            # asegurar que existan todas las claves
            for k, v in defaults.items():
                if k not in loaded:
                    loaded[k] = v
            return loaded
    except Exception:
        return defaults


def save_settings(settings):
    with open(DATA_SETTINGS, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


# -------------------------
# VARIABLES "globales" de UI
# -------------------------
class ImportantVars:
    bradius: float = 20.0
    ctitle: int = 20
    ctext: int = 17
    first_launch: bool = False


# Paletas / Colores
class Colors2:
    Base = "#4A5A95EC"
    # Paleta Pro (oscura)
    Profl_Fondo = "#121828"
    Profl_FondoSecundario = "#1E293B"
    Profl_TextoPrincipal = "#C5D6E8FF"
    Profl_Acento1 = "#445187FF"
    Profl_Acento2 = "#354172FF"
    # Tec
    Tec_Fondo = "#770D50FF"
    Tec_Texto = "#E994E7FF"
    Tec_Acento1 = "#C60CC9E4"
    Tec_Acento2 = "#9E288EFF"
    # Pastel
    Pastel_Fondo = "#477D5AFF"
    Pastel_Secundario = "#3A852EFF"
    Pastel_Acento1 = Base
    Pastel_Acento2 = "#377129FF"
    Pastel_TextoOscuro = "#B1E8AEFF"
    # Elegante
    Elegante_Fondo = "#000000FF"
    Elegante_FondoSecundario = "#000000FF"
    Elegante_Texto = "#E0E6ED"
    Elegante_Acento1 = "#000000FF"
    Elegante_Acento2 = "#000000FF"
    # Dorado
    Df = "#EEC336FF"
    Dfs = "#D49E27FF"
    Dt = "#E6D18EFF"
    Da1 = "#EEC336FF"
    Da2 = "#D49E27FF"


THEMES = ["Pro", "Tec", "Pastel", "Elegante", "Golden"]
FONT_SIZES = ["1", "2", "3"]
RADIUS_OPTIONS = ["0", "5", "10", "15", "20", "25", "30"]


def get_theme_colors(theme_name):
    """Devuelve un dict con colores según el nombre del tema."""
    if theme_name == "Pro":
        return {
            "bg": Colors2.Profl_Fondo,
            "bg2": Colors2.Profl_FondoSecundario,
            "text": Colors2.Profl_TextoPrincipal,
            "a1": Colors2.Profl_Acento1,
            "a2": Colors2.Profl_Acento2,
        }
    if theme_name == "Tec":
        return {
            "bg": Colors2.Tec_Fondo,
            "bg2": Colors2.Tec_Fondo,
            "text": Colors2.Tec_Texto,
            "a1": Colors2.Tec_Acento1,
            "a2": Colors2.Tec_Acento2,
        }
    if theme_name == "Pastel":
        return {
            "bg": Colors2.Pastel_Fondo,
            "bg2": Colors2.Pastel_Secundario,
            "text": Colors2.Pastel_TextoOscuro,
            "a1": Colors2.Pastel_Acento1,
            "a2": Colors2.Pastel_Acento2,
        }
    if theme_name == "Elegante":
        return {
            "bg": Colors2.Elegante_Fondo,
            "bg2": Colors2.Elegante_FondoSecundario,
            "text": Colors2.Elegante_Texto,
            "a1": Colors2.Elegante_Acento1,
            "a2": Colors2.Elegante_Acento2,
        }
    # Golden / fallback
    return {
        "bg": Colors2.Df,
        "bg2": Colors2.Dfs,
        "text": Colors2.Dt,
        "a1": Colors2.Da1,
        "a2": Colors2.Da2,
    }


# -------------------------
# FUNCIONES DE DATOS
# -------------------------
def cargar_datos():
    """Lee contenedores desde JSON; devuelve lista vacía si no hay o está corrupto."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def guardar_datos(lista):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


# -------------------------
# APP PRINCIPAL
# -------------------------
def main(page: ft.Page):
    # Cargar settings al inicio (una sola vez)
    settings = load_settings()
    ImportantVars.bradius = float(settings.get("bradius", 20.0))

    # Ajustar tamaños de fuente iniciales
    xs = settings.get("font_size", "2")
    if xs == "1":
        ImportantVars.ctitle = 15
        ImportantVars.ctext = 12
    elif xs == "2":
        ImportantVars.ctitle = 20
        ImportantVars.ctext = 17
    elif xs == "3":
        ImportantVars.ctitle = 25
        ImportantVars.ctext = 22

    THEME = get_theme_colors(settings.get("theme", "Pro"))

    page.title = "Notes"
    page.window_full_screen = True
    page.window_frameless = True
    page.bgcolor = THEME["bg"]
    page.padding = 12

    # Elementos reusables
    # GRID donde se muestran las notas (solo Type == 1)
    lista_contenedores = ft.GridView(
        expand=True,
        runs_count=0,
        max_extent=220,
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        spacing=10,
        run_spacing=10,
    )

    # Cargar datos
    data = cargar_datos()

    # -------------------------
    # CREAR CONTENEDOR (NOTA)
    # -------------------------
    def crear_contenedor_nota(index: int, item: dict) -> ft.Container:
        """Construye y devuelve un ft.Container para una nota (Type == 1)."""
        # Botón de eliminar (aparece en la parte superior del contenedor)
        delete_button = ft.Container(
            bgcolor=THEME["a1"],
            scale=0,
            height=0,
            animate_size=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
            animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_IN_OUT),
            border_radius=ImportantVars.bradius,
            border=ft.border.all(1, THEME["a2"]),
            content=ft.Row(
                controls=[
                    ft.Switch(
                        thumb_icon=ft.Icons.DELETE,
                        expand=True,
                        inactive_track_color=THEME["a2"],
                        active_color="red",
                        active_track_color="red",
                        on_change=lambda e, idx=index: eliminar(idx),
                    )
                ],
                spacing=0,
            ),
        )

        # Column con preview (si está activada la previsualización)
        if settings.get("preview", True):
            content_column = ft.Column(
                controls=[
                    delete_button,
                    ft.Container(
                        margin=ft.margin.only(bottom=45),
                        content=ft.Column(
                            controls=[
                                ft.Text(item.get("nombre", "Sin título"), weight="bold", size=ImportantVars.ctitle, color=THEME["text"]),
                                ft.Text(item.get("text", ""), weight="bold", size=ImportantVars.ctext, color=THEME["text"], expand=True),
                            ]
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        else:
            content_column = ft.Column(
                controls=[
                    delete_button,
                    ft.Container(
                        margin=ft.margin.only(bottom=45),
                        content=ft.Column(
                            controls=[
                                ft.Text(item.get("nombre", "Sin título"), weight="bold", size=ImportantVars.ctitle, color=THEME["text"]),
                                ft.Text("", weight="bold", size=ImportantVars.ctext, color=THEME["text"], expand=True),
                            ]
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        cont = ft.Container(
            on_click=lambda e, idx=index: ir_a_editar(e, idx),
            gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[THEME["bg"], THEME["bg2"]]),
            height=50,
            width=200,
            border_radius=ImportantVars.bradius,
            padding=10,
            scale=1,
            on_animation_end=lambda e: content_column.update(),
            animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
            opacity=0,
            animate_size=ft.Animation(600, ft.AnimationCurve.BOUNCE_IN_OUT),
            border=ft.border.all(1, THEME["a2"]),
            content=content_column,
        )

        cont.opacity = 1
        cont.offset = ft.Offset(0, 0)
        return cont

    # -------------------------
    # RENDERIZAR LISTA (solo notas)
    # -------------------------
    def render_lista():
        lista_contenedores.controls.clear()
        for idx, item in enumerate(data):
            # Solo renderizamos items de Type == 1 (notas). Ignoramos cualquier otro tipo.
            if item.get("Type", 1) == 1:
                lista_contenedores.controls.append(crear_contenedor_nota(idx, item))
        page.update()

    render_lista()

    # -------------------------
    # ELIMINAR ITEM
    # -------------------------
    def eliminar(idx: int):
        if 0 <= idx < len(data):
            data.pop(idx)
            guardar_datos(data)
            render_lista()
            page.update()

    # -------------------------
    # ANIMACION: mostrar/ocultar botones eliminar
    # -------------------------
    def reapariton_of_delete_button(e):
        for cont in lista_contenedores.controls:
            aparitionButton = cont.content.controls[0]  # asumimos que el primer control es el DeleteButton
            aparitionButton.scale = 1 if aparitionButton.scale == 0 else 0
            aparitionButton.height = None if aparitionButton.height == 0 else 0
        page.update()

    # -------------------------
    # NAVEGACION BASICA
    # -------------------------
    def ir_a_form(e):
        page.go("/form")
        note_text.scale = 1
        separation.height = 0



    def volver_a_inicio(e):
        page.go("/")
        # Si el SearchBar está visible, ocultarlo
        page.update()


    def ir_a_editar(e, index: int):
        page.go(f"/edit/{index}")


    def go_to_settings(e):
        page.go('/settings')


    # -------------------------
    # UI SUPERIOR
    # -------------------------
    tra = ft.Container(
        bgcolor=THEME["bg2"],
        animate_size=ft.Animation(600, ft.AnimationCurve.BOUNCE_OUT),
        height=35,
        width=50,
        padding=ft.padding.only(left=12),
        on_click=lambda e: chage_tra(e),
        border_radius=ImportantVars.bradius,
        content=ft.Row(
            alignment=ft.alignment.center,
            controls=[
                ft.Icon(ft.Icons.MENU, color=THEME["text"]),
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, on_click=lambda e: go_to_settings(e), icon_color=THEME["text"]),
            ],
        ),
    )

    # cambia tamaño del tra (menu)
    def chage_tra(e):
        tra.height = 70 if tra.height == 35 else 35
        tra.width = 250 if tra.width == 50 else 50
        tra.shadow = (
            ft.BoxShadow(
                spread_radius=1,
                blur_radius=3,
                color=THEME["a2"],
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
            if tra.shadow is None
            else None
        )

        render_lista()

        page.update()

    # mostrar/ocultar buscador
    def change_seek(e):
        if seeker.scale == 0:
            seeker.value = ""
            # Mostrar buscador
            seeker.scale = 1
            seeker.height = 50
            separation.height = 50
            note_text.scale = 0
            seeker.disabled = False
            page.update()
            seeker.focus()
        else:
            # Ocultar buscador
            seeker.value = ""
            seeker.scale = 0
            seeker.height = 0
            separation.height = 0
            seeker.disabled = True
            page.update()
            note_text.scale = 1
            
            render_lista()  # restaurar lista completa

        page.update()

    note_text = ft.Container(
        content=ft.Text("Notes", size=30, color=THEME["text"]),
        padding=ft.padding.only(left=11, top=11),
        animate_size=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(600, ft.AnimationCurve.BOUNCE_IN_OUT),
    )

    # -------------------------
    # PICKERS Y SETTINGS UI
    # -------------------------
    select_fonts_ref = ft.Ref[ft.Text]()
    select_fruit_ref = ft.Ref[ft.Text]()
    select_radius_ref = ft.Ref[ft.Text]()

    def handle_picker_change(e):
        # e.data es el índice
        idx = int(e.data)
        if 0 <= idx < len(THEMES):
            select_fruit_ref.current.value = THEMES[idx]
        page.update()

    def handle_picker_fs_change(e):
        idx = int(e.data)
        if 0 <= idx < len(FONT_SIZES):
            select_fonts_ref.current.value = FONT_SIZES[idx]
        page.update()

    def handle_picker_rd_change(e):
        idx = int(e.data)
        if 0 <= idx < len(RADIUS_OPTIONS):
            select_radius_ref.current.value = RADIUS_OPTIONS[idx]
        page.update()

    cupertino_picker = ft.CupertinoPicker(
        selected_index=0,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_picker_change,
        controls=[ft.Text(value=f) for f in THEMES],
    )

    cupertino_FS_picker = ft.CupertinoPicker(
        selected_index=0,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_picker_fs_change,
        controls=[ft.Text(value=f) for f in FONT_SIZES],
    )

    cupertino_RD_picker = ft.CupertinoPicker(
        selected_index=0,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=handle_picker_rd_change,
        controls=[ft.Text(value=f) for f in RADIUS_OPTIONS],
    )

    # Mensajes informativos
    importan_mensaje_theme = ft.Text(
        "Reinicie la app para aplicar el tema",
        size=12,
        color=THEME["text"],
        height=0,
        animate_size=ft.Animation(600, ft.AnimationCurve.FAST_OUT_SLOWIN),
    )

    importan_mensaje_radius = ft.Text(
        "Reinicie la app para aplicar el radio del borde",
        size=12,
        color=THEME["text"],
        height=0,
        animate_size=ft.Animation(600, ft.AnimationCurve.FAST_OUT_SLOWIN),
    )

    # Dialogo y funciones aplicar
    themedialog = ft.AlertDialog(
        title=ft.Text("Aplicar Tema"),
        bgcolor=THEME["a2"],
        actions=[
            ft.ElevatedButton("Aceptar", on_click=lambda e: aplic_theme(e)),
        ],
        content=ft.Text("El tema ha sido aplicado. Por favor reinicia la aplicación."),
    )

    def aplic_theme(e):
        # aplicar el tema seleccionado en el picker
        nuevo = select_fruit_ref.current.value if select_fruit_ref.current else settings.get("theme")
        change_theme(nuevo)
        page.dialog = None
        page.close_dialog()
        page.update()

    # Select buttons (muestran pickers en bottom sheet)
    change_text_button = ft.TextButton(
        content=ft.Text(value=settings.get("theme", "Pro"), ref=select_fruit_ref, size=20, color=THEME["text"]),
        on_click=lambda e: page.open(
            ft.CupertinoBottomSheet(cupertino_picker, height=216, on_dismiss=lambda ev: change_theme(select_fruit_ref.current.value if select_fruit_ref.current else settings.get("theme")))
        ),
    )

    change_size_button = ft.TextButton(
        content=ft.Text(value=settings.get("font_size", "2"), ref=select_fonts_ref, size=20, color=THEME["text"]),
        on_click=lambda e: page.open(
            ft.CupertinoBottomSheet(cupertino_FS_picker, height=216, on_dismiss=lambda ev: change_font_size(select_fonts_ref.current.value if select_fonts_ref.current else settings.get("font_size")))
        ),
    )

    change_radius_button = ft.TextButton(
        content=ft.Text(value=str(settings.get("bradius", 20.0)), ref=select_radius_ref, size=20, color=THEME["text"]),
        on_click=lambda e: page.open(
            ft.CupertinoBottomSheet(cupertino_RD_picker, height=216, on_dismiss=lambda ev: change_radius(select_radius_ref.current.value if select_radius_ref.current else str(settings.get("bradius"))))
        ),
    )

    resetValuebutton = ft.IconButton(
        icon=ft.Icons.SETTINGS_BACKUP_RESTORE,
        icon_color=THEME["text"],
        height=0,
        scale=0,
        width=0,
        animate_size=ft.Animation(600, ft.AnimationCurve.FAST_OUT_SLOWIN),
        on_click=lambda e: reset_radius(),
    )

    def reset_radius():
        settings["bradius"] = 20.0
        save_settings(settings)
        ImportantVars.bradius = settings["bradius"]
        importan_mensaje_radius.height = None
        select_radius_ref.current.value = "20" if select_radius_ref.current else "20"
        render_lista()
        page.update()

    def change_radius(radius_value):
        try:
            r = float(radius_value)
        except Exception:
            r = 20.0
        settings["bradius"] = r
        save_settings(settings)
        ImportantVars.bradius = r
        importan_mensaje_radius.height = None
        render_lista()
        page.update()

    def change_font_size(number):
        if number == "1":
            ImportantVars.ctitle = 15
            ImportantVars.ctext = 12
            settings["font_size"] = number
        elif number == "2":
            ImportantVars.ctitle = 20
            ImportantVars.ctext = 17
            settings["font_size"] = number
        elif number == "3":
            ImportantVars.ctitle = 25
            ImportantVars.ctext = 22
            settings["font_size"] = number
        save_settings(settings)
        render_lista()

    def change_theme(name):
        # 1. Guardar ajustes
        settings["theme"] = name
        save_settings(settings)
        # 2. Actualizar THEME global (redefinimos variable local)
        nonlocal_theme = get_theme_colors(name)
        importan_mensaje_theme.height = None
        # Actualizar el fondo de la página
        page.bgcolor = nonlocal_theme["bg"]
        # re-asignar THEME (mutamos el objeto que usan los controles en este scope)
        for k in THEME.keys():
            THEME[k] = nonlocal_theme[k]
        render_lista()
        page.go(page.route)
        page.update()

    def change_preview(e):
        settings["preview"] = True if preview.value else False
        save_settings(settings)
        render_lista()
    


    preview = ft.Switch(on_change=change_preview, value=settings.get("preview", True))
    separation = ft.Container(height=0)

    # -------------------------
    # RUTAS: VISTAS
    # -------------------------
    def route_change(route):
        page.views.clear()

        # PANTALLA PRINCIPAL
        if page.route == "/":
            page.views.append(
                ft.View(
                    padding=ft.padding.only(left=12, right=12, bottom=12, top=12),
                    route="/",
                    controls=[
                        separation,
                        note_text,
                        ft.Divider(),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    lista_contenedores,
                                    ft.Container(width=0, height=0, visible=False),
                                ]
                            ),
                            expand=True,
                            padding=10,
                            border_radius=ImportantVars.bradius,
                        ),
                        ft.Container(
                            height=60,
                            alignment=ft.alignment.center_right,
                            on_long_press=reapariton_of_delete_button,
                            content=ft.Row(
                                expand=True,
                                controls=[
                                    ft.Container(margin=10, content=tra),
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.alignment.center_right,
                                        content=ft.IconButton(
                                            icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE,
                                            bgcolor=ft.Colors.TRANSPARENT,
                                            on_click=ir_a_form,
                                            icon_color=THEME["text"],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            )

        # PANTALLA DE AJUSTES
        elif page.route.startswith("/settings"):
            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[
                        ft.Container(
                            margin=ft.margin.only(top=30),
                            height=50,
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_SHARP, on_click=volver_a_inicio, icon_color=THEME["text"]),
                                    ft.Text("Settings", size=20, color=THEME["text"]),
                                ]
                            ),
                        ),
                        ft.Container(
                            padding=10,
                            border_radius=ImportantVars.bradius,
                            border=ft.border.all(1, THEME["a1"]),
                            bgcolor=THEME["a2"],
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Seleccionar tema", size=18, color=THEME["text"]),
                                            ft.Container(expand=True),
                                            ft.Container(alignment=ft.alignment.center_right, content=change_text_button),
                                        ]
                                    ),
                                    importan_mensaje_theme,
                                    ft.Divider(color=THEME["text"]),
                                    ft.Row(
                                        controls=[ft.Text("Tamaño de fuente", size=18, color=THEME["text"]), ft.Container(expand=True), change_size_button]
                                    ),
                                    ft.Divider(color=THEME["text"]),
                                    ft.Row(controls=[ft.Text("Previsualización", size=18, color=THEME["text"]), ft.Container(expand=True), preview]),
                                    ft.Divider(color=THEME["text"]),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Radio del borde", size=18, color=THEME["text"]),
                                            ft.Container(expand=True),
                                            change_radius_button,
                                            resetValuebutton,
                                        ]
                                    ),
                                    importan_mensaje_radius,
                                ]
                            ),
                        ),
                        ft.Container(expand=True),
                    ],
                )
            )

        # PANTALLA FORM (crear / editar nota)
        elif page.route.startswith("/form") or page.route.startswith("/edit"):
            
            text_field_main = ft.TextField(multiline=True, expand=True, border_width=0, border_radius=30, text_size=18,)
            nombre_field = ft.TextField(border_width=0, border_radius=30, text_size=25, hint_text='Título')
            preview_markdown = ft.Markdown(value="", selectable=True, expand=True, )

        

            is_edit = page.route.startswith("/edit")
            item_index = -1
            initial_name = ""
            initial_color = THEME["bg"]
            initial_color2 = THEME["bg2"]
            initial_preview = False

            def toggle_preview(e):
                value = settings['pw']
                if value == False:
                    # Cambiar a PREVIEW
                    preview_markdown.value = text_field_main.value
                    editor_container.content = preview_markdown
                    settings['pw'] = True
                    save_settings(settings)
                else:
                    # Volver a modo EDICIÓN
                    editor_container.content = text_field_main
                    settings['pw'] = False
                    save_settings(settings)

                page.update()
            
            preview_switch = ft.Switch(label="Preview", value=False, on_change=toggle_preview)

            editor_container = ft.Container(
                expand=True,
                content=text_field_main,  # inicia en modo edición
            )

            if is_edit:
                try:
                    item_index = int(page.route.split("/")[-1])
                    if 0 <= item_index < len(data):
                        item_data = data[item_index]
                        initial_name = item_data.get("nombre", "")
                        initial_color = item_data.get("color", THEME["bg"])
                        initial_color2 = item_data.get("color2", THEME["bg2"])
                        text_field_main.value = item_data.get("text", "")
                        initial_preview = item_data.get("pw", "")
                    else:
                        page.go("/")
                        page.update()
                        return
                except ValueError:
                    page.go("/")
                    page.update()
                    return
                nombre_field.value = initial_name
                Color = initial_color
                Color2 = initial_color2
            else:
                # creación
                nombre_field.value = ""
                Color = THEME["bg"]
                Color2 = THEME["bg2"]
                text_field_main.value = ""

            def guardar_o_editar(e):
                nombre = nombre_field.value or "Sin nombre"
                color = Color or "#FFFFFF"
                color2 = Color2 or "#FFFFFF"
                TextValue = text_field_main.value or ""

                if not color.startswith("#"):
                    color = "#" + color
                if not color2.startswith("#"):
                    color2 = "#" + color2

                nuevo_item = {
                    "Type": 1,
                    "nombre": nombre,
                    "color": color,
                    "color2": color2,
                    "text": TextValue,
                    "pw": initial_preview
                }

                if is_edit:
                    if 0 <= item_index < len(data):
                        data[item_index] = nuevo_item
                    else:
                        return
                else:
                    data.append(nuevo_item)

                guardar_datos(data)
                render_lista()
                page.go("/")

            # color contrast calculation para el campo (simple)
            try:
                hex_color = color.lstrip("#")
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
                text_color = ft.Colors.BLACK if luminance > 0.5 else ft.Colors.WHITE
            except Exception:
                text_color = ft.Colors.WHITE

            nombre_field.color = text_color
            text_field_main.color = text_color

            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            nombre_field,
                                            ft.Divider(),
                                            editor_container,
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        margin=ft.margin.only(top=0),
                                                        content=ft.IconButton(icon=ft.Icons.CLOSE, on_click=volver_a_inicio, bgcolor=ft.Colors.TRANSPARENT, icon_color=THEME["text"]),
                                                        expand=True,
                                                        on_long_press=toggle_preview,
                                                        alignment=ft.alignment.center_left,    
                                                    ),
                                                    ft.IconButton(icon=ft.Icons.CHECK, on_click=guardar_o_editar, bgcolor=ft.Colors.TRANSPARENT, icon_color=THEME["text"]),
                                                ]
                                            ),
                                        ]
                                    ),
                                    expand=True,
                                    margin=ft.margin.only(top=11),
                                    padding=5,
                                    gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[THEME["bg"], THEME["bg2"]]),
                                    bgcolor=Color,
                                    border=ft.border.all(1, Color),
                                    border_radius=ImportantVars.bradius,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=3,
                                        color=Color,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                                ),
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            spacing=20,
                        )
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)
