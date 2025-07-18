from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk
import numpy as np

class Representation:
    Points = 0
    Wireframe = 1
    Surface = 2
    SurfaceWithEdges = 3

def update_representation(actor, mode):
    """Обновление типа отображения актора"""
    property = actor.GetProperty()
    if mode == Representation.Points:
        property.SetRepresentationToPoints()
        property.SetPointSize(5)
        property.EdgeVisibilityOff()
    elif mode == Representation.Wireframe:
        property.SetRepresentationToWireframe()
        property.SetPointSize(1)
        property.EdgeVisibilityOff()
    elif mode == Representation.Surface:
        property.SetRepresentationToSurface()
        property.SetPointSize(1)
        property.EdgeVisibilityOff()
    elif mode == Representation.SurfaceWithEdges:
        property.SetRepresentationToSurface()
        property.SetPointSize(1)
        property.EdgeVisibilityOn()

def color_by_array(actor, array, component_idx=0, reader=None):
    """Окрашивание меша по массиву данных"""
    mapper = actor.GetMapper()
    if array is None or array.get("text") == "Geometry":
        mapper.SetScalarVisibility(False)
        actor.GetProperty().SetColor(0.7, 0.7, 0.7)
    else:
        _min, _max = array.get("range")
        n_components = array.get("n_components", 1)
        array_name = array.get("text")
        
        # Получаем данные
        data = reader.GetOutput()
        if n_components == 1:
            # Скалярный массив
            mapper.SelectColorArray(array_name)
            mapper.GetLookupTable().SetRange(_min, _max)
            if array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
                mapper.SetScalarModeToUsePointFieldData()
            else:
                mapper.SetScalarModeToUseCellFieldData()
            mapper.SetScalarVisibility(True)
            mapper.SetUseLookupTableScalarRange(True)
        else:
            # Векторный массив
            if array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
                arr = data.GetPointData().GetArray(array_name)
                pd = data.GetPointData()
            else:
                arr = data.GetCellData().GetArray(array_name)
                pd = data.GetCellData()
            
            np_arr = vtk_to_numpy(arr)
            if component_idx == -1:
                # Модуль вектора
                scalar_data = np.linalg.norm(np_arr, axis=1)
            else:
                scalar_data = np_arr[:, component_idx]
            
            vtk_scalar = numpy_to_vtk(scalar_data)
            vtk_scalar.SetName("tmp_scalar")
            pd.AddArray(vtk_scalar)
            mapper.SelectColorArray("tmp_scalar")
            mapper.GetLookupTable().SetRange(float(np.min(scalar_data)), float(np.max(scalar_data)))
            
            if array.get("type") == vtkDataObject.FIELD_ASSOCIATION_POINTS:
                mapper.SetScalarModeToUsePointFieldData()
            else:
                mapper.SetScalarModeToUseCellFieldData()
            mapper.SetScalarVisibility(True)
            mapper.SetUseLookupTableScalarRange(True)

def setup_mesh_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays):
    """Настройка контроллеров для управления мешем"""
    
    # Получаем актор меша (первый актор в рендерере)
    actors = renderer.GetActors()
    actors.InitTraversal()
    mesh_actor = actors.GetNextActor()
    
    @state.change("mesh_representation")
    def update_mesh_representation(mesh_representation, **kwargs):
        update_representation(mesh_actor, mesh_representation)
        ctrl.view_update()
    
    @state.change("mesh_color_array_idx", "mesh_vector_component")
    def update_mesh_color(mesh_color_array_idx, mesh_vector_component, **kwargs):
        array = dataset_arrays[mesh_color_array_idx]
        color_by_array(mesh_actor, array, mesh_vector_component, reader)
        ctrl.view_update() 