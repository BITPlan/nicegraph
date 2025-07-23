"""
Created on 2025-07-23

@author: wf
"""

import re

import i18n
from basemkit.persistent_log import Log
from mogwai.core.mogwaigraph import MogwaiGraph
from mogwai.schema.graph_schema import GraphSchema
from mogwai.web.node_view import NodeTableView, NodeView, NodeViewConfig
from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from nicegui import Client, ui


class GraphNavigatorWebserver(InputWebserver):
    """
    Graph navigation Webserver
    """

    def __init__(self, config):
        """Constructs all the necessary attributes for the WebServer object."""
        InputWebserver.__init__(self, config=config)
        self.log = Log()

        @ui.page("/nodes/{node_type}")
        async def show_nodes(client: Client, node_type: str):
            """
            show the nodes of the given type
            """
            await self.page(client, GraphNavigatorSolution.show_nodes, node_type)

        @ui.page("/node/{node_type}/{node_id}")
        async def node(client: Client, node_type: str, node_id: str):
            """
            show the node with the given node_id
            """
            await self.page(
                client, GraphNavigatorSolution.show_node, node_type, node_id
            )

    def configure_run(self):
        """
        configure with args
        """
        self.graph = MogwaiGraph()

    def load_schema(self, yaml_path: str):
        self.schema = GraphSchema.load(yaml_path=yaml_path)
        self.schema.add_to_graph(self.graph)


class GraphNavigatorSolution(InputWebSolution):
    """
    Graph navigation User interface
    """

    def __init__(self, webserver: GraphNavigatorWebserver, client: Client):
        """
        Initialize the solution

        Calls the constructor of the base solution
        Args:
            webserver (UsercodeWebServer): The webserver instance associated with this context.
            client (Client): The client instance this context is associated with.
        """
        super().__init__(webserver, client)  # Call to the superclass constructor#
        self.log = webserver.log
        self.graph = webserver.graph
        self.schema = webserver.schema

    def prepare_ui(self):
        """
        prepare the user interface
        """
        anchor_style = r"a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}"
        ui.add_head_html(f"<style>{anchor_style}</style>")
        # set the user interface language
        accept_language = self.client.request.headers.get("accept-language", "")
        match = re.search(r"(?P<primary_language>[a-zA-Z\-]+)", accept_language)
        self.primary_language = match.group("primary_language") if match else None
        i18n.set("locale", self.primary_language)
        pass

    def configure_menu(self):
        """
        configure additional non-standard menu entries
        """
        # Sorting the node types by display_order
        sorted_node_types = sorted(
            self.schema.node_type_configs.items(),
            key=lambda item: item[1].display_order,
        )

        for node_type_name, node_type in sorted_node_types:  # label e.g. project_list
            label_i18nkey = f"{node_type.label.lower()}_list"
            label = i18n.t(label_i18nkey)
            path = f"/nodes/{node_type_name}"
            self.link_button(label, path, node_type.icon, new_tab=False)
        if self.primary_language:
            ui.label(f"{self.primary_language}")

    async def show_nodes(self, node_type: str):
        """
        show nodes of the given type

        Args:
            node_type(str): the type of nodes to show
        """

        def show():
            try:
                config = NodeViewConfig(
                    solution=self,
                    graph=self.graph,
                    schema=self.schema,
                    node_type=node_type,
                )
                if not config.node_type_config:
                    ui.label(f"{i18n.t('invalid_node_type')}: {node_type}")
                    return
                node_table_view = NodeTableView(config=config)
                node_table_view.setup_ui()
            except Exception as ex:
                self.handle_exception(ex)

        await self.setup_content_div(show)

    async def show_node(self, node_type: str, node_id: str):
        """
        show the given node
        """

        def show():
            config = NodeViewConfig(
                solution=self, graph=self.graph, schema=self.schema, node_type=node_type
            )
            if not config.node_type_config:
                ui.label(f"{i18n.t('invalid_node_type')}: {node_type}")
                return
            # default view is the general NodeView
            view_class = NodeView
            # unless there is a specialization configured
            if config.node_type_config._viewclass:
                view_class = config.node_type_config._viewclass
            node_view = view_class(config=config, node_id=node_id)
            node_view.setup_ui()
            pass

        await self.setup_content_div(show)
