class LookupTable:
    Rainbow = 0
    Inverted_Rainbow = 1
    Greyscale = 2
    Inverted_Greyscale = 3

def use_preset(actor, preset):
    """Применение предустановленной цветовой карты"""
    lut = actor.GetMapper().GetLookupTable()
    if preset == LookupTable.Rainbow:
        lut.SetHueRange(0.666, 0.0)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
    elif preset == LookupTable.Inverted_Rainbow:
        lut.SetHueRange(0.0, 0.666)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
    elif preset == LookupTable.Greyscale:
        lut.SetHueRange(0.0, 0.0)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(0.0, 1.0)
    elif preset == LookupTable.Inverted_Greyscale:
        lut.SetHueRange(0.0, 0.666)
        lut.SetSaturationRange(0.0, 0.0)
        lut.SetValueRange(1.0, 0.0)
    lut.Build()

def setup_color_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor, reader, dataset_arrays):
    """Настройка контроллеров для управления цветом"""
    
    # Получаем актор меша (первый актор в рендерере)
    actors = renderer.GetActors()
    actors.InitTraversal()
    mesh_actor = actors.GetNextActor()
    
    @state.change("mesh_color_preset")
    def update_mesh_color_preset(mesh_color_preset, **kwargs):
        use_preset(mesh_actor, mesh_color_preset)
        ctrl.view_update() 