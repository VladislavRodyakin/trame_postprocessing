import os
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch
import vtkmodules.vtkRenderingOpenGL2

def setup_vtk_pipeline():
    """Инициализация VTK pipeline"""
    
    # Получение абсолютного пути к текущей директории
    current_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Создание рендерера
    renderer = vtkRenderer()
    
    # Создание окна рендеринга
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    
    # Создание интерактора
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    
    # Чтение VTK файла
    file_path = os.path.join(current_directory, "results_1.vtk")

    reader = vtkUnstructuredGridReader()
    reader.SetFileName(file_path)
    reader.Update()
    
    # Извлечение информации о массивах данных
    dataset_arrays = []
    fields = [
        (reader.GetOutput().GetPointData(), vtkDataObject.FIELD_ASSOCIATION_POINTS),
        (reader.GetOutput().GetCellData(), vtkDataObject.FIELD_ASSOCIATION_CELLS),
    ]
    
    for field in fields:
        field_arrays, association = field
        for i in range(field_arrays.GetNumberOfArrays()):
            array = field_arrays.GetArray(i)
            if array is None:
                continue
            array_range = array.GetRange()
            n_components = array.GetNumberOfComponents()
            dataset_arrays.append({
                "text": array.GetName(),
                "value": i,
                "range": list(array_range),
                "type": association,
                "n_components": n_components
            })
    
    # Добавление опции "Geometry"
    dataset_arrays.insert(0, {
        "text": "Geometry",
        "value": 0,
        "range": [0, 1],
        "type": None,
        "n_components": 1,
    })
    
    # Создание меша
    mesh_mapper = vtkDataSetMapper()
    mesh_mapper.SetInputConnection(reader.GetOutputPort())
    
    mesh_actor = vtkActor()
    mesh_actor.SetMapper(mesh_mapper)
    renderer.AddActor(mesh_actor)
    
    # Настройка отображения по умолчанию
    mesh_actor.GetProperty().SetRepresentationToSurface()
    mesh_actor.GetProperty().SetPointSize(1)
    mesh_actor.GetProperty().EdgeVisibilityOff()
    mesh_actor.GetProperty().SetColor(0.7, 0.7, 0.7)
    mesh_mapper.SetScalarVisibility(False)
    
    # Создание координатных осей
    cube_axes = vtkCubeAxesActor()
    renderer.AddActor(cube_axes)
    
    cube_axes.SetBounds(mesh_actor.GetBounds())
    cube_axes.SetCamera(renderer.GetActiveCamera())
    cube_axes.SetXLabelFormat("%6.1f")
    cube_axes.SetYLabelFormat("%6.1f")
    cube_axes.SetZLabelFormat("%6.1f")
    cube_axes.SetFlyModeToOuterEdges()
    
    # Сброс камеры
    renderer.ResetCamera()
    
    return renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays 

#  TODO working on it
# def update_vtk_pipeline(reader, dataset_arrays):
#     """Обновление VTK pipeline"""

#     # Обновление меша
#     mesh_mapper = reader.GetOutputPort()
#     mesh_actor.SetMapper(mesh_mapper)

#     # Обновление координатных осей
#     cube_axes = reader.GetOutputPort()
#     cube_axes.SetCamera(renderer.GetActiveCamera())
#     cube_axes.SetXLabelFormat("%6.1f")
#     cube_axes.SetYLabelFormat("%6.1f")
#     cube_axes.SetZLabelFormat("%6.1f")
#     cube_axes.SetFlyModeToOuterEdges()

#     # Сброс камеры
#     renderer.ResetCamera()

#     return renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays