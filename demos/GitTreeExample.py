from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, trame
import uuid
import os

# Инициализация сервера
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# Структура для хранения файлов и папок
state.nodes = [
    {
        "id": 'root',
        "parent": '0',
        "visible": 1,
        "name": "Главная папка",
        'type': 'folder',
        'icon': 'mdi-folder',
        'open': True,  # Папка открыта по умолчанию
        'content': None
    }
]

state.open_nodes = ['root']  # ID открытых узлов
state.active_file = None
state.file_content = "Выберите файл для просмотра"
state.new_file_name = ""

# Состояние для контекстного меню
state.context_menu_open = False
state.context_menu_x = 0
state.context_menu_y = 0
state.context_menu_file = None

# Функции для работы с файлами
def add_file():
    """Добавляет новый файл в корневую папку"""
    if not state.new_file_name:
        return

    if os.path.exists(state.new_file_name):
        try:
            # Читаем содержимое файла
            with open(state.new_file_name, 'r', encoding='cp1251') as f:
                    new_node = {
                    "id": str(uuid.uuid4()),
                    "parent": "0",
                    "visible": 1,
                    "name": state.new_file_name,
                    'type': 'file',
                    'icon': 'mdi-file-document',
                    'open': True,
                    'content': f.read()
                }
            # Добавляем новый узел в состояние
            
            state.nodes.append(new_node)
            state.new_file_name = ""
            state.pipeline = state.nodes.copy()
            # state.flush("pipeline")
            state.flush()

        except Exception as e:
            print(f"Ошибка при чтении файла:\n{str(e)}")
    else:
        print(f"Файл не найден")

# Функция удаления файла
def delete_file(node_id):
    if  node_id == 'root': #not node_id or
        return  # Нельзя удалить корневую папку
    
    # 1. Находим все ID для удаления (сам узел + все потомки)
    ids_to_remove = set()
    stack = [node_id]
    
    while stack:
        current_id = stack.pop()
        ids_to_remove.add(current_id)
        
        # Находим всех прямых потомков текущего узла
        children_ids = [node['id'] for node in state.nodes if node['parent'] == current_id]
        stack.extend(children_ids)
    
    # 2. Создаем новый список узлов без удаляемых элементов
    new_nodes = [node for node in state.nodes if node['id'] not in ids_to_remove]
    
    # 3. Обновляем состояние
    state.nodes = new_nodes
    
    # 4. Если активный узел был удален - сбрасываем его
    if state.active_node and state.active_node in ids_to_remove:
        state.active_node = None
    
    # 5. Обновляем UI
    state.pipeline = state.nodes.copy()
    # state.flush("pipeline")
    state.flush()
    print(f"Удалено узлов: {len(ids_to_remove)}")

# Удаление активного файла
def delete_active_file():
    delete_file(state.active_node)

# Удаление файла из контекстного меню
def delete_context_file():
    if state.context_menu_file:
        delete_file(state.context_menu_node_id)

# Открытие контекстного меню
def open_context_menu(file, event):
    """Открывает контекстное меню для файла"""
    state.context_menu_file = file
    state.context_menu_open = True
    state.context_menu_x = event.clientX
    state.context_menu_y = event.clientY

# Регистрация функций в контроллере
ctrl.delete_active_file = delete_active_file
ctrl.delete_context_file = delete_context_file
ctrl.open_context_menu = open_context_menu

# Обработчик выбора элемента в дереве
def on_tree_select(items):
    """Вызывается при выборе элемента в дереве"""
    if items and len(items) > 0:
        item = items[0]
        if item:
            state.active_file = item
            if item['type'] == 'file':
                state.file_content = f"должно быть содержание файла '{item['name']}'" 
    else:
        state.active_file = None
        state.file_content = "Выберите файл для просмотра"

state.new_file_name = "t1.csv"
add_file()
state.new_file_name = ""

# Создание интерфейса
with SinglePageLayout(server) as layout:
    layout.title.set_text("Авиарасчеты")

    with layout.content:
        with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
            with vuetify.VRow(style="height: 100%;"):
                # Левая панель - дерево файлов и форма добавления
                with vuetify.VCol(cols=4, classes="pa-0"):
                    with vuetify.VCard(height="100%", classes="elevation-2 d-flex flex-column"):
                        # Форма добавления файла
                        with vuetify.VCardTitle("Шаг 1"):
                            vuetify.VTextField(
                                v_model=("new_file_name"),
                                label="Имя файла",
                                outlined=True,
                                dense=True,
                                hide_details=True
                            )

                        vuetify.VBtn(
                            "Добавить файл", 
                            click=add_file,
                            color="primary",
                            classes="ma-2"
                        )

                        vuetify.VDivider(classes="my-2")
                        
                        with vuetify.VCardText(style="overflow-y: auto; flex-grow: 1;"):

                            trame.GitTree(
                                sources=("pipeline", state.nodes),
                                # actives_change=(print(1), "[$event]"),
                                # visibility_change=(delete_active_file, "[$event]"),

                                # open_nodes=("open_nodes",),  # Управление открытыми узлами
                                # update_open_nodes=(lambda e: state.assign(open_nodes=e), "[$event]"),
                                # activatable=True,
                                # open_on_click=True,
                                # item_key="id",
                                # item_text="name",
                                # # Опциональные параметры:
                                # dense=True,
                                # hoverable=True,
                                # show_visibility=False  # Скрыть контролы видимости  
                            )

                            vuetify.VDivider(classes="mb-2")

                            with vuetify.VCardActions():
                                vuetify.VBtn(
                                    "Delete",
                                    color="error",
                                    icon="mdi-delete",
                                    classes="ma-2",
                                    click=delete_active_file
                                )
                

if __name__ == "__main__":
    server.start()