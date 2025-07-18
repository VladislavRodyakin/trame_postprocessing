from logic.vtk_pipeline import setup_vtk_pipeline
from logic.mesh_controls import setup_mesh_controls
from logic.color_controls import setup_color_controls
from logic.view_controls import setup_view_controls
# from trame.decorators import hot_reload

# @hot_reload
def setup_3D_state_and_controllers(state, ctrl, content=None):
    # print(content)
    # Инициализация VTK pipeline
    renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays = setup_vtk_pipeline(content)
    
    # Состояние для отображения
    state.cube_axes_visibility = True
    state.mesh_representation = 2  # Surface по умолчанию
    state.mesh_color_array_idx = 0
    state.mesh_color_preset = 0  # Rainbow по умолчанию
    state.mesh_vector_component = 0
    
    # Состояние для UI
    state.representations = [
        {"text": "Points", "value": 0},
        {"text": "Wireframe", "value": 1},
        {"text": "Surface", "value": 2},
        {"text": "SurfaceWithEdges", "value": 3},
    ]
    
    state.array_list = dataset_arrays
    state.colormaps = [
        {"text": "Rainbow", "value": 0},
        {"text": "Inv Rainbow", "value": 1},
        {"text": "Greyscale", "value": 2},
        {"text": "Inv Greyscale", "value": 3},
    ]
    
    state.opti = [
        {"text": "X", "value": 0},
        {"text": "Y", "value": 1},
        {"text": "Z", "value": 2},
        {"text": "Magnitude", "value": -1},
    ]
    
    # Pipeline для отображения
    state.pipeline = [
        {"id": "1", "parent": "0", "visible": 1, "name": "Mesh"},
    ]
    
    # Сохраняем VTK объекты в состоянии для доступа из макета

# TODO Этот блок выдаёт некритичные для работы ошибки
# Error: Skip state value for 'vtk_renderer' since its content is not serializable
    # state.vtk_renderer = renderer
    state.vtk_renderWindow = renderWindow
    # state.vtk_renderWindowInteractor = renderWindowInteractor
    # state.vtk_reader = reader


    state.vtk_dataset_arrays = dataset_arrays

    # Настройка контроллеров
    setup_mesh_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays)
    setup_color_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays)
    setup_view_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor)
