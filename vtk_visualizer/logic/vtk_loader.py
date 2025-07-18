import vtk, os
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader


# def load_csv_content(content):
#     reader = csv.DictReader(io.StringIO(content), delimiter=';')
#     data = [row for row in reader]
#     headers = [{"text": k, "value": k} for k in data[0].keys()] if data else []
#     return data, headers

def load_vtk_content(content):
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader