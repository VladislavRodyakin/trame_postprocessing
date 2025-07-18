from logic.csv_loader import load_csv_content
from logic.vtk_loader import load_vtk_content

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
            elif item['name'].lower().endswith('.vtk'):
                previous_vtk_reader = state.vtk_reader
                previous_vtk_dataset_arrays = state.dataset_arrays
                try:
                    reader, dataset_arrays = load_vtk_content(item['content'])
                    state.vtk_reader = reader
                    state.vtk_dataset_arrays = dataset_arrays
                    # TODO вызвать обновление визуализации
                except Exception as e:
                    print(f"Ошибка загрузки CSV: {e}")
                    state.vtk_reader = previous_vtk_reader
                    state.vtk_dataset_arrays = previous_vtk_dataset_arrays
            else:
                state.table_data = []
                state.headers = []
    else:
        state.active_file = None
        state.table_data = []
        state.headers = [] 