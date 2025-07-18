def delete_file_from_tree(state):
    if not state.active_file or state.active_file.get('type') != 'file':
        return
    if not state.files or not state.files[0] or 'children' not in state.files[0]:
        return
    
    file_id = state.active_file['id']
    # Копируем дерево, чтобы реактивность сработала
    new_files = state.files.copy()
    root = {**new_files[0]}
    new_children = [child for child in root['children'] if child['id'] != file_id]
    root['children'] = new_children
    new_files[0] = root
    state.files = new_files
    state.active_file = None
    state.table_data = []
    state.headers = []

    # Обновление ключа для форс-обновления дерева
    state.files_key += 1
    state.selected_file = None
