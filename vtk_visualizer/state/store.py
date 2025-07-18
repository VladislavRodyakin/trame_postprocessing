from state.state_3D import setup_3D_state_and_controllers
from state.state_tree import setup_tree_state_and_controllers


def setup_state_and_controllers(state, ctrl):
    setup_tree_state_and_controllers(state, ctrl)
    setup_3D_state_and_controllers(state, ctrl)
