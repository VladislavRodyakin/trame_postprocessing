from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify

server = get_server(client_type="vue2")
if server is None:
    raise RuntimeError("Trame server could not be initialized. Check your trame installation.")

state = server.state

# Проверяем, инициализирован ли список опций для выпадающего меню
# Если нет — создаём список значений от 1 до 10
if getattr(state, "options", None) is None:
    state.options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Проверяем, инициализирована ли строка для отображения выбранного значения
# Если нет — задаём стартовую подсказку для пользователя
if getattr(state, "selected_label", None) is None:
    state.selected_label = "если нажать на кнопку, то будет выведено значение"

# Функция-обработчик изменения значения в выпадающем списке
# При выборе нового значения обновляет строку для отображения на сайте
# (теперь в поле под списком появится надпись с выбранным значением)
def on_select_change(value):
    state.selected_label = f"Выбрано новое значение: {value}"

with SinglePageLayout(server) as layout:
    layout.title.set_text("Выбор значения")
    with layout.content:
        # Выпадающий список с вариантами выбора
        # При изменении значения вызывается функция on_select_change
        vuetify.VSelect(
            v_model=("selected_value", None),
            items=("options", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            label="Варианты",
            change=(on_select_change, "[$event]"),
        )
        # Поле для отображения выбранного значения или подсказки
        # Значение берётся из state.selected_label и обновляется автоматически
        vuetify.VTextField(label="", v_model=("selected_label", ""), readonly=True)

if __name__ == "__main__":
    server.start()