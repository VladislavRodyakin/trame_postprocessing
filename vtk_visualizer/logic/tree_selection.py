from logic.csv_loader import load_csv_content
from logic.vtk_loader import load_vtk_content
from logic.vtk_pipeline import update_vtk_pipeline
from state.state_3D import setup_3D_state_and_controllers

def handle_tree_selection(items, state, ctrl):
    if items:
        item = items[0]
        state.active_file = item  # обновляем активный файл
        if item.get('type') == 'file':
            # print(item['name'].lower())
            if item['name'].lower().endswith('.csv'):
                # print('read as CSV')
                try:
                    data, headers = load_csv_content(item['content'])
                    state.table_data = data
                    state.headers = headers
                except Exception as e:
                    print(f"Ошибка загрузки CSV: {e}")
                    state.table_data = []
                    state.headers = []
            elif item['name'].lower().endswith('.vtk'):
                print(item['name'])
                previous_vtk_dataset_arrays = state.dataset_arrays
                try:
                    # _, dataset_arrays = load_vtk_content(item['content'])
                    # state.vtk_dataset_arrays = dataset_arrays
                    setup_3D_state_and_controllers(state, ctrl, item['content'])
                    
                except Exception as e:
                    print(f"Ошибка загрузки VTK: {e}")
                    state.vtk_dataset_arrays = previous_vtk_dataset_arrays
            else:
                state.table_data = []
                state.headers = []
    else:
        state.active_file = None
        state.table_data = []
        state.headers = [] 