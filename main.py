import flet as ft

productos = [
    {
        "id": 1,
        "nombre": "MacBook Pro",
        "descripcion": "Chip M3 Pro · 18 GB RAM · 512 GB SSD",
        "precio": 2_499.99,
        "ruta_imagen": "macbook_pro.png",
    },
    {
        "id": 2,
        "nombre": "iPhone 15",
        "descripcion": "6.1\" OLED · Dynamic Island · USB-C",
        "precio": 999.99,
        "ruta_imagen": "iphone_15.png",
    },
    {
        "id": 3,
        "nombre": "Dell XPS 15",
        "descripcion": "Intel i9 · 32 GB RAM · RTX 4060",
        "precio": 1_899.99,
        "ruta_imagen": "dell_xps.jpeg",
    },
    {
        "id": 4,
        "nombre": "Teclado Keychron",
        "descripcion": "K2 Pro · Inalámbrico · Switch Red",
        "precio": 119.99,
        "ruta_imagen": "teclado_keychron.jpeg",
    },
    {
        "id": 5,
        "nombre": "Mouse Logitech",
        "descripcion": "MX Master 3S · 8K DPI · Silencioso",
        "precio": 99.99,
        "ruta_imagen": "mouse_logitech.jpeg",
    },
]

class ProductoCard(ft.Container):

    def __init__(self, producto, page, carrito_text, favoritos_text, carrito, favoritos):
        super().__init__()

        self.producto = producto
        self.mi_pagina = page
        self.es_favorito = False
        self.carrito_text = carrito_text
        self.favoritos_text = favoritos_text
        self.carrito = carrito
        self.favoritos = favoritos

        self.icono_favorito = ft.Icon(ft.Icons.FAVORITE_BORDER, size=16, color=ft.Colors.BLACK)
        self.texto_favorito = ft.Text("Favorito", color=ft.Colors.BLACK)

        self.btn_favorito = ft.ElevatedButton(
            content=ft.Row(
                [self.icono_favorito, self.texto_favorito],
                tight=True,
                spacing=4,
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=2),
                side=ft.BorderSide(1, ft.Colors.BLACK),
            ),
            on_click=self._toggle_favorito,
        )

        btn_agregar = ft.ElevatedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.ADD, size=16, color=ft.Colors.WHITE), ft.Text("Agregar", color=ft.Colors.WHITE)],
                tight=True,
                spacing=4,
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLACK,
                shape=ft.RoundedRectangleBorder(radius=2),
            ),
            on_click=self._agregar_carrito,
        )

        self.content = ft.Column(
            spacing=12,
            controls=[
                ft.Container(
                    content=ft.Image(
                        src=producto["ruta_imagen"],
                        height=150,
                        fit="contain",
                    ),
                    alignment=ft.Alignment.CENTER,
                    padding=ft.padding.only(top=12, bottom=4),
                ),
                ft.Text(
                    producto["nombre"],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    producto["descripcion"],
                    size=11,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    f"${producto['precio']:,.2f} USD",
                    size=18,
                    weight=ft.FontWeight.W_900,
                    color=ft.Colors.GREEN_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    controls=[self.btn_favorito, btn_agregar],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
        )

        self.bgcolor = ft.Colors.WHITE
        self.border_radius = 12
        self.width = 280
        self.padding = 20
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        )
        self.col = {"xs": 12, "sm": 6, "md": 4, "lg": 3}

    def _mostrar_snackbar(self, mensaje):
        snack = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.BLACK,
            duration=2000,
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        self.mi_pagina.overlay.append(snack)
        snack.open = True
        self.mi_pagina.update()

    def _toggle_favorito(self, e):
        self.es_favorito = not self.es_favorito

        if self.es_favorito:
            self.favoritos.append(self.producto["id"])
            self.icono_favorito.name = ft.Icons.FAVORITE
            self.icono_favorito.color = ft.Colors.RED
            self._mostrar_snackbar(f"Añadido a favoritos: {self.producto['nombre']}")
        else:
            self.favoritos.remove(self.producto["id"])
            self.icono_favorito.name = ft.Icons.FAVORITE_BORDER
            self.icono_favorito.color = ft.Colors.BLACK
            self._mostrar_snackbar(f"Quitado de favoritos: {self.producto['nombre']}")

        self.favoritos_text.value = str(len(self.favoritos))
        self.favoritos_text.update()
        self.icono_favorito.update()

    def _agregar_carrito(self, e):
        self.carrito.append(self.producto["id"])
        self.carrito_text.value = str(len(self.carrito))
        self.carrito_text.update()
        self._mostrar_snackbar(f"Agregado al carrito: {self.producto['nombre']}")


def main(page: ft.Page):
    page.title = "PCTECH Catalog"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F7F7F7"
    page.padding = 32
    page.scroll = ft.ScrollMode.AUTO

    carrito = []
    favoritos = []

    carrito_text = ft.Text("0", size=14, weight=ft.FontWeight.W_900, color=ft.Colors.WHITE)
    favoritos_text = ft.Text("0", size=14, weight=ft.FontWeight.W_900, color=ft.Colors.BLACK)

    dlg_carrito = ft.AlertDialog(
        title=ft.Text("CARRITO", weight=ft.FontWeight.W_900, color=ft.Colors.BLACK),
        bgcolor=ft.Colors.WHITE,
        title_padding=24,
        content_padding=24,
    )
    
    dlg_favoritos = ft.AlertDialog(
        title=ft.Text("FAVORITOS", weight=ft.FontWeight.W_900, color=ft.Colors.BLACK),
        bgcolor=ft.Colors.WHITE,
        title_padding=24,
        content_padding=24,
    )

    page.overlay.extend([dlg_carrito, dlg_favoritos])

    def cerrar_carrito(e):
        dlg_carrito.open = False
        page.update()

    def cerrar_favoritos(e):
        dlg_favoritos.open = False
        page.update()

    def ver_carrito(e):
        if not carrito:
            contenido = ft.Text("Tu carrito está vacío.", color=ft.Colors.BLACK)
        else:
            articulos = []
            total = 0
            for prod_id in carrito:
                for p in productos:
                    if p["id"] == prod_id:
                        articulos.append(ft.Text(f"• {p['nombre']} - ${p['precio']:,.2f}", color=ft.Colors.BLACK))
                        total += p["precio"]
                        break
            
            contenido = ft.Column(
                controls=articulos + [
                    ft.Divider(color=ft.Colors.BLACK, thickness=2),
                    ft.Text(f"TOTAL: ${total:,.2f} USD", weight=ft.FontWeight.W_900, size=18, color=ft.Colors.BLACK)
                ],
                tight=True,
            )

        btn_pagar = ft.ElevatedButton(
            "PROCEDER AL PAGO",
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLACK,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=2)
            ),
            on_click=cerrar_carrito
        )
        btn_cerrar = ft.TextButton("CERRAR", style=ft.ButtonStyle(color=ft.Colors.BLACK), on_click=cerrar_carrito)

        dlg_carrito.content = contenido
        dlg_carrito.actions = [btn_pagar if carrito else ft.Container(), btn_cerrar]
        dlg_carrito.open = True
        page.update()

    def ver_favoritos(e):
        if not favoritos:
            contenido = ft.Text("No hay artículos guardados.", color=ft.Colors.BLACK)
        else:
            articulos = []
            para_mostrar = set(favoritos)
            for prod_id in para_mostrar:
                for p in productos:
                    if p["id"] == prod_id:
                        articulos.append(ft.Text(f"• {p['nombre']}", color=ft.Colors.BLACK))
                        break
            
            contenido = ft.Column(controls=articulos, tight=True)

        btn_cerrar = ft.TextButton("CERRAR", style=ft.ButtonStyle(color=ft.Colors.BLACK), on_click=cerrar_favoritos)

        dlg_favoritos.content = contenido
        dlg_favoritos.actions = [btn_cerrar]
        dlg_favoritos.open = True
        page.update()

    carrito_chip = ft.Container(
        content=carrito_text,
        bgcolor=ft.Colors.BLACK,
        border_radius=4,
        padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
        on_click=ver_carrito,
        tooltip="Ver Carrito"
    )

    favoritos_chip = ft.Container(
        content=favoritos_text,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=4,
        padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
        on_click=ver_favoritos,
        tooltip="Ver Favoritos"
    )

    encabezado = ft.Container(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Text(
                    "PCTECH.",
                    size=42,
                    weight=ft.FontWeight.W_900,
                    color=ft.Colors.BLACK,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "PREMIUM HARDWARE",
                    size=12,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                    style=ft.TextStyle(letter_spacing=2),
                ),
                ft.Container(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=32,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.IconButton(ft.Icons.SHOPPING_BAG_OUTLINED, icon_color=ft.Colors.BLACK, on_click=ver_carrito),
                                ft.Text("CARRITO", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                                carrito_chip,
                            ],
                        ),
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.IconButton(ft.Icons.FAVORITE_BORDER, icon_color=ft.Colors.BLACK, on_click=ver_favoritos),
                                ft.Text("GUARDADO", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD),
                                favoritos_chip,
                            ],
                        ),
                    ],
                ),
                ft.Divider(color=ft.Colors.BLACK, thickness=2, height=40),
            ],
        ),
        margin=ft.margin.only(bottom=24),
    )

    catalogo = ft.ResponsiveRow(
        columns=12,
        spacing=24,
        run_spacing=24,
        controls=[
            ProductoCard(p, page, carrito_text, favoritos_text, carrito, favoritos)
            for p in productos
        ],
    )

    footer = ft.Container(
        content=ft.Text(
            "© 2026 PCTECH. ALL RIGHTS RESERVED.",
            size=10,
            color=ft.Colors.GREY_500,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        margin=ft.margin.only(top=48),
        alignment=ft.Alignment.CENTER,
    )

    page.add(encabezado, catalogo, footer)

ft.run(
    main,
    assets_dir="assets"
)