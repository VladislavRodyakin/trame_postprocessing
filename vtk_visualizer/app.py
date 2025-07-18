from trame.app import get_server
from layout.main_layout import build_layout
from state.store import setup_state_and_controllers

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller
setup_state_and_controllers(state, ctrl)

build_layout(server)

if __name__ == "__main__":
    server.start() 