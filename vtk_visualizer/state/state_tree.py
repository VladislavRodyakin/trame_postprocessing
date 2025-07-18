# from logic.csv_loader import load_csv_content
from logic.add_file import add_file_to_tree
from logic.delete_file import delete_file_from_tree
from logic.tree_selection import handle_tree_selection


def setup_tree_state_and_controllers(state, ctrl):
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
    
    state.files_key = 0
    state.selected_file = None
    state.active_file = None
    state.table_data = []
    state.headers = []

    ctrl.on_add_file = lambda: add_file_to_tree(state)
    ctrl.on_tree_select = lambda items: handle_tree_selection(items, state)
    ctrl.on_delete_file = lambda: delete_file_from_tree(state)

    @state.change("selected_file")
    def on_file_selected(**_):
        add_file_to_tree(state)