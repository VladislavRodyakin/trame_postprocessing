from logic.csv_loader import load_csv_content

def handle_tree_selection(items, state):
    if items:
        item = items[0]
        state.active_file = item  # обновляем активный файл
        if item.get('type') == 'file':
            if item['name'].lower().endswith('.csv'):
                try:
                    data, headers = load_csv_content(item['content'])
                    state.table_data = data
                    state.headers = headers
                except Exception as e:
                    print(f"Ошибка загрузки CSV: {e}")
                    state.table_data = []
                    state.headers = []
            else:
                state.table_data = []
                state.headers = []
    else:
        state.active_file = None
        state.table_data = []
        state.headers = [] 