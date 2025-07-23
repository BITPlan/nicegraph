"""
Created on 2025-07-23

@author: wf
"""

from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from ngwidgets.webserver import WebserverConfig
from nicegui import Client, ui

from ng3.version import Version


class GraphNavigatorDemoSolution(InputWebSolution):
    """
    Graph Navigator Demo Solution
    """

    def __init__(self, webserver: "GraphNavigatorDemoWebserver", client: Client):
        """
        Initialize the demo solution

        Args:
            webserver: The webserver instance
            client: The client instance
        """
        super().__init__(webserver, client)

    async def home(self):
        """
        Provide the main content page
        """

        def setup_home():
            ui.label("Welcome")

        await self.setup_content_div(setup_home)


class GraphNavigatorDemoWebserver(InputWebserver):
    """
    Graph navigator demo webserver
    """

    @classmethod
    def get_config(cls) -> WebserverConfig:
        """
        Get the webserver configuration

        Returns:
            WebserverConfig: The server configuration
        """
        copy_right = "(c)2024-2025 Wolfgang Fahl"
        config = WebserverConfig(
            short_name="ng3demo",
            copy_right=copy_right,
            version=Version(),
            default_port=9853,
        )
        server_config = WebserverConfig.get(config)
        server_config.solution_class = GraphNavigatorDemoSolution
        return server_config

    def __init__(self):
        """
        Constructor
        """
        InputWebserver.__init__(self, config=GraphNavigatorDemoWebserver.get_config())
