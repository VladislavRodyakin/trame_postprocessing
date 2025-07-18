import uuid

def add_file_to_tree(state):
    file_info = state.selected_file
    print("Добавление файла:", file_info)  # Для отладки
    if not file_info:
        return
    
    if isinstance(file_info, list):
        file_info = file_info[0]

    if 'content' not in file_info:
        print("⚠️ Файл не содержит контента")
        return
    
    new_file = {
        'id': str(uuid.uuid4()),
        'name': file_info['name'],
        'type': 'file',
        'icon': 'mdi-file-document',
        'content': file_info['content'].decode('cp1251', errors='replace')
    }

# TODO ДАЛЬШЕ - ЗАМЕНЯЕМ НА ДЕРЕВО ПОЛИНЫ
    # Копируем дерево, чтобы реактивность сработала
    new_files = state.files.copy()
    root = {**new_files[0]}
    new_children = root['children'].copy()
    new_children.append(new_file)
    root['children'] = new_children
    new_files[0] = root
    state.files = new_files


# TODO ДОБАВИТЬ В ДЕРЕВО ПОЛИНЫ
    if getattr(state, "files_key", None) is None:
        state.files_key = 1
    else:
        state.files_key += 1 