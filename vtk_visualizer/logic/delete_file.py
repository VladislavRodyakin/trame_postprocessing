def delete_file_from_tree(state):

    # 1. Находим все ID для удаления (сам узел + все потомки)
    # ids_to_remove = set()
    # stack = [state.selected_file]
    # print(state.selected_file)
    # while stack:
    #     current_id = stack.pop()
    #     ids_to_remove.add(current_id)
        
        # Находим всех прямых потомков текущего узла
        # children_ids = [file['id'] for file in state.nodes if file['parent'] == current_id]
        # stack.extend(children_ids)
    
    # # 2. Создаем новый список узлов без удаляемых элементов
    # new_files = [file for file in state.files if file['id'] not in ids_to_remove]
    
    # # 3. Обновляем состояние
    # state.files = new_files
    
    # # 4. Если активный узел был удален - сбрасываем его
    # if state.active_file and state.active_file in ids_to_remove:
    #     state.active_file = None
    
    # # 5. Обновляем UI
    # state.pipeline = state.files.copy()
    state.selected_file = None
    # # state.flush("pipeline")
    # state.flush()

    # if not state.active_file or state.active_file.get('type') != 'file':
    #     return
    # if not state.files or not state.files[0] or 'children' not in state.files[0]:
    #     return
    
    # file_id = state.active_file['id']
    # # Копируем дерево, чтобы реактивность сработала
    # new_files = state.files.copy()
    # root = {**new_files[0]}
    # new_children = [child for child in root['children'] if child['id'] != file_id]
    # root['children'] = new_children
    # new_files[0] = root
    # state.files = new_files
    # state.active_file = None
    # state.table_data = []
    # state.headers = []

    # Обновление ключа для форс-обновления дерева
    state.files_key += 1
    state.selected_file = None
