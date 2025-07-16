from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, html
import uuid
import csv
import io

server = get_server(client_type="vue2")
state = server.state
ctrl = server.controller

# Изначально только корневая папка
state.files = [
    {
        'id': 'root',
        'name': 'Главная папка',
        'type': 'folder',
        'icon': 'mdi-folder',
        'children': [],
        'open': True
    }
]
state.selected_file = None
state.active_file = None
state.table_data = []
state.headers = []
state.files_key = 0  # ключ для форс-обновления дерева

# === Функция для загрузки данных из CSV ===
def load_csv_content(content):
    reader = csv.DictReader(io.StringIO(content), delimiter=';')
    data = [row for row in reader]
    headers = [{"text": k, "value": k} for k in data[0].keys()] if data else []
    return data, headers

# Обработчик выбора элемента в дереве
def on_tree_select(items):
    if items and len(items) > 0:
        item = items[0]
        if item and item.get('type') == 'file':
            # Если CSV - загружаем таблицу
            if item['name'].lower().endswith('.csv'):
                try:
                    data, headers = load_csv_content(item['content'])
                    state.table_data = data
                    state.headers = headers
                except Exception:
                    state.table_data = []
                    state.headers = []
            else:
                # Для не-CSV файлов очищаем таблицу
                state.table_data = []
                state.headers = []
        state.active_file = item
    else:
        state.active_file = None
        state.table_data = []
        state.headers = []

# Добавление выбранного файла в дерево
def on_add_file():
    file_info = state.selected_file
    if not file_info:
        return
    if isinstance(file_info, list):
        file_info = file_info[0]
    # Проверка на наличие контента
    if 'content' not in file_info:
        return
    new_file = {
        'id': str(uuid.uuid4()),
        'name': file_info['name'],
        'type': 'file',
        'icon': 'mdi-file-document',
        'content': file_info['content'].decode('cp1251', errors='replace')
    }
    new_files = state.files.copy()
    root = {**new_files[0]}
    new_children = root['children'].copy()
    new_children.append(new_file)
    root['children'] = new_children
    new_files[0] = root
    state.files = new_files
    state.selected_file = None
    if state.files_key is None:
        state.files_key = 1
    else:
        state.files_key += 1

# Удаление выбранного файла из дерева
def on_delete_file():
    if not state.active_file or state.active_file.get('type') != 'file':
        return
    if not state.files or not state.files[0] or 'children' not in state.files[0]:
        return
    file_id = state.active_file['id']
    new_children = [child for child in state.files[0]['children'] if child['id'] != file_id]
    updated_folder = {**state.files[0], 'children': new_children}
    state.files = [updated_folder]
    state.active_file = None
    state.table_data = []
    state.headers = []
    if state.files_key is None:
        state.files_key = 1
    else:
        state.files_key += 1

# Явно регистрируем функции в контроллере
ctrl.on_add_file = on_add_file
ctrl.on_tree_select = on_tree_select
ctrl.on_delete_file = on_delete_file

with SinglePageLayout(server) as layout:
    layout.title.set_text("Авиарасчеты")
    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vuetify.VRow(style="height: 100%;"):
                with vuetify.VCol(cols=4, classes="pa-0"):
                    with vuetify.VCard(height="100%", classes="elevation-2 d-flex flex-column"):
                        with vuetify.VCardTitle("Шаг 1"):
                            vuetify.VFileInput(
                                v_model=("selected_file",),
                                label="Выберите файл",
                                outlined=True,
                                dense=True,
                                hide_details=True,
                                accept="*",
                                multiple=False,
                            )
                            vuetify.VBtn(
                                "Добавить файл",
                                click=ctrl.on_add_file,
                                color="primary",
                                classes="ma-2"
                            )
                        vuetify.VDivider(classes="my-2")
                        with vuetify.VCardText(style="overflow-y: auto; flex-grow: 1;"):
                            vuetify.VTreeview(
                                items=("files",),
                                activatable=True,
                                open_on_click=True,
                                dense=True,
                                return_object=True,
                                item_key="id",
                                item_text="name",
                                item_children="children",
                                v_model=("active_file", None),
                                open_all=True,
                                key=("files_key", "files_key"),
                                update_active=(ctrl.on_tree_select, "[$event]")
                            )
                            vuetify.VBtn(
                                v_if=("active_file && active_file.type === 'file'",),
                                color="error",
                                classes="ma-2",
                                click=ctrl.on_delete_file,
                                children=[
                                    vuetify.VIcon("mdi-delete", color="white"),
                                ]
                            )
                # Правая панель - таблица
                with vuetify.VCol(cols=8, classes="pa-0"):
                    with vuetify.VCard(style="height: 350px; margin-top: 300px;", classes="elevation-2 d-flex flex-column"):
                        vuetify.VCardTitle("Просмотр содержимого")
                        # Обёртка с прокруткой для таблицы
                        with vuetify.VContainer(
                            v_if=("table_data && table_data.length > 0",),
                            style="height: 250px; overflow-y: auto; padding: 0;"
                        ):
                            vuetify.VDataTable(
                                items=("table_data",),
                                headers=("headers",),
                                hide_default_footer=True,
                                density="compact",
                                items_per_page=-1,
                            )

if __name__ == "__main__":
    server.start()