from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vtk, vuetify, trame

def standard_buttons():
    """Стандартные кнопки управления"""
    # Чекбокс для отображения/скрытия координатных осей
    vuetify.VCheckbox(
        v_model=("cube_axes_visibility", True),
        on_icon="mdi-cube-outline",
        off_icon="mdi-cube-off-outline",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    # Чекбокс для переключения светлой/тёмной темы интерфейса
    vuetify.VCheckbox(
        v_model="$vuetify.theme.dark",
        on_icon="mdi-lightbulb-off-outline",
        off_icon="mdi-lightbulb-outline",
        classes="mx-1",
        hide_details=True,
        dense=True,
    )
    # Кнопка для сброса камеры
    with vuetify.VBtn(icon=True, click="$refs.view.resetCamera()"):
        vuetify.VIcon("mdi-crop-free")

def pipeline_widget():
    """Виджет для отображения pipeline"""
    trame.GitTree(
        sources=(
            "pipeline",
            [
                {"id": "1", "parent": "0", "visible": 1, "name": "Mesh"},
            ],
        ),
    )

def mesh_card():
    """Карточка управления параметрами меша"""
    with vuetify.VCard():
        vuetify.VCardTitle(
            "Mesh",
            classes="grey lighten-1 py-1 grey--text text--darken-3",
            style="user-select: none; cursor: pointer",
            hide_details=True,
            dense=True,
        )
        # Контейнер для содержимого карточки
        with vuetify.VCardText(classes="py-2"):
            # Выбор типа отображения
            vuetify.VSelect(
                v_model=("mesh_representation", 2),
                items=(
                    "representations",
                    [
                        {"text": "Points", "value": 0},
                        {"text": "Wireframe", "value": 1},
                        {"text": "Surface", "value": 2},
                        {"text": "SurfaceWithEdges", "value": 3},
                    ],
                ),
                label="Representation",
                hide_details=True,
                dense=True,
                outlined=True,
                classes="pt-1",
            )
            # Блок для выбора массива для окрашивания и цветовой карты
            with vuetify.VRow(classes="pt-2", dense=True):
                with vuetify.VCol(cols="4"):
                    # Выбор массива для окрашивания
                    vuetify.VSelect(
                        label="Color by",
                        v_model=("mesh_color_array_idx", 0),
                        items=("array_list", []),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
                
                with vuetify.VCol(cols="4"):
                    # Выбор цветовой карты
                    vuetify.VSelect(
                        label="Colormap",
                        v_model=("mesh_color_preset", 0),
                        items=(
                            "colormaps",
                            [
                                {"text": "Rainbow", "value": 0},
                                {"text": "Inv Rainbow", "value": 1},
                                {"text": "Greyscale", "value": 2},
                                {"text": "Inv Greyscale", "value": 3},
                            ],
                        ),
                        hide_details=True,
                        dense=True,
                        outlined=True,
                        classes="pt-1",
                    )
            with vuetify.VRow(style="margin-top: 20px;"):
                with vuetify.VCol(cols="6"):
                    vuetify.VSelect(
                        label="Component",
                        v_model=("mesh_vector_component", 0),
                        items=('opti', [
                            {"text": "X", "value": 0},
                            {"text": "Y", "value": 1},
                            {"text": "Z", "value": 2},
                            {"text": "Magnitude", "value": -1},
                        ]),
                        outlined=True,
                        classes="pt-1",
                        v_show="array_list[mesh_color_array_idx].n_components > 1",
                    )

def left_panel(state, ctrl):
    with vuetify.VCard(height="100%", classes="elevation-2 d-flex flex-column"):
                        with vuetify.VCardTitle("Шаг 1"):
                            vuetify.VFileInput(
                                v_model=("selected_file",),
                                label="Выберите файл",
                                outlined=True,
                                dense=True,
                                hide_details=True,
                                accept="*",
                                multiple=False
                            )
                            
                        vuetify.VDivider(classes="my-2")

                        with vuetify.VCardText(style="overflow-y: auto; flex-grow: 1;"):
                            vuetify.VTreeview(
                                items=("files",),
                                activatable=True,
                                open_on_click=True,
                                dense=True,
                                return_object=True,
                                item_key="id",
                                item_text="name",
                                item_children="children",
                                v_model=("active_file", None),
                                open_all=True,
                                key=("files_key"),
                                update_active=(ctrl.on_tree_select, "[$event]")
                            )
                            vuetify.VBtn(
                                v_if=("active_file && active_file.type === 'file'",),
                                color="error",
                                classes="ma-2",
                                click=ctrl.on_delete_file,
                                children=[
                                    vuetify.VIcon("mdi-delete", color="white"),
                                ]
                            )


def build_layout(server):
    """Построение главного макета приложения"""
    state, ctrl = server.state, server.controller
    
    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("VTK Visualizer")
        
        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VDivider(vertical=True, classes="mx-2")
            standard_buttons()
        
        with layout.drawer as drawer:
            drawer.width = '25%'
            pipeline_widget()
            vuetify.VDivider(classes="mb-2")
            mesh_card()
            left_panel(state, ctrl)

        
        with layout.content:
            with vuetify.VContainer(
                fluid=True,
                classes="pa-0 fill-height",
            ):
                # Используем renderWindow из состояния
                view = vtk.VtkLocalView(state.vtk_renderWindow)
                ctrl.view_update = view.update
                ctrl.view_reset_camera = view.reset_camera 