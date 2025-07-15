from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify
import csv

server = get_server(client_type="vue2")
if server is None:
    raise RuntimeError("Trame server could not be initialized. Check your trame installation.")

state = server.state

# === Функция для загрузки данных из CSV ===
def load_csv_to_state(state, filename):
    with open(filename, encoding="cp1251") as f:
        reader = csv.DictReader(f, delimiter=';')  # Указан разделитель ';' для вашего файла
        data = [row for row in reader]
        state.table_data = data
        # Заголовки (названия столбцов)
        if data:
            state.headers = [{"text": k, "value": k} for k in data[0].keys()]
            state.column_names = list(data[0].keys())
        else:
            state.headers = []
            state.column_names = []
        state.row_count = len(data)
        state.col_count = len(state.column_names)

# === Загрузка данных из файла ===
load_csv_to_state(state, "table.csv")  # <-- Теперь берёт данные из table.csv

with SinglePageLayout(server) as layout:
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-4"):
            with vuetify.VRow(justify="center"):
                with vuetify.VCol(cols="12", sm="6"):
                    with vuetify.VCard(style="height: 300px;"):
                        vuetify.VCardTitle("Данные из CSV", classes="text-h5")
                       
                        # Обёртка с прокруткой для таблицы
                        with vuetify.VContainer(style="height: 200px; overflow-y: auto; padding: 0;"):
                            vuetify.VDataTable(
                                items=("table_data",),
                                headers=("headers",),
                                hide_default_footer=True,
                                density="compact",
                            )

if __name__ == "__main__":
    server.start()