def setup_view_controls(state, ctrl, renderer, renderWindow, renderWindowInteractor):
    """Настройка контроллеров для управления видом"""
    
    # Получаем актор координатных осей (второй актор в рендерере)
    actors = renderer.GetActors()
    actors.InitTraversal()
    mesh_actor = actors.GetNextActor()
    cube_axes = actors.GetNextActor()
    
    @state.change("cube_axes_visibility")
    def update_cube_axes_visibility(cube_axes_visibility, **kwargs):
        cube_axes.SetVisibility(cube_axes_visibility)
        ctrl.view_update() 