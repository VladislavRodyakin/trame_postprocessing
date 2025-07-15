from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")
if server is None:
    raise RuntimeError("Trame server could not be initialized. Check your trame installation.")

def increment():
    print("Button clicked!")

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-4"):  # Контейнер с отступами
            # Заголовок по центру
            with vuetify.VRow(justify="center"):
                vuetify.VCol(cols="12", md="8")
                vuetify.VCardTitle("Демонстрация сетки", classes="text-center")
            # Основной контент
            with vuetify.VRow():
                # Левая панель (25% ширины)
                with vuetify.VCol(cols="12", sm="3"):
                    vuetify.VCard("Навигация", style="height: 300px;")
                # Центральный контент (50%)
                with vuetify.VCol(cols="12", sm="6"):
                    with vuetify.VRow():
                        with vuetify.VCol(cols="6"):
                            with vuetify.VCard(style="height: 120px;"):
                                vuetify.VCardTitle("Не важная информация")
                                vuetify.VCardText("перед тобой две библиотеки - конвертор и конвектор")
                        with vuetify.VCol(cols="6"):
                            with vuetify.VCard(style="height: 120px;"):
                                vuetify.VCardTitle("Важная информация")
                                vuetify.VCardText("Выбери какую сам используешь, какую друзьям посоветуешь")
                    vuetify.VCard("Основной контент", style="height: 200px; margin-top: 20px;")
                    # Пример нескольких кнопок
                    for _ in range(8):
                        vuetify.VBtn("Нажми меня!", click=increment)
                # Правая панель (25%)
                with vuetify.VCol(cols="12", sm="3"):
                    vuetify.VCard("Информация", style="height: 300px;")
            # Нижний колонтитул
            with vuetify.VRow(style="margin-top: 20px;"):
                vuetify.VCol(cols="12")
                vuetify.VFooter("Футер", absolute=True)

if __name__ == "__main__":
    server.start()