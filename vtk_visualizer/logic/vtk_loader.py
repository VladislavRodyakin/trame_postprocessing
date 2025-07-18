import io
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader

def load_vtk_content(content):
    """Инициализация VTK pipeline"""
    
    # Чтение VTK файла
    # file_path = os.path.join(current_directory, "results_1.vtk")
    
    reader = vtkUnstructuredGridReader() 
    # reader.SetFileName(file_path) # TODO try changing to SetInputString
    reader.SetInputString(io.StringIO(content))
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

    return reader, dataset_arrays
