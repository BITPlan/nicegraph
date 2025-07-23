"""
Created on 2025-07-23

@author: wf
"""

import sys

from ngwidgets.cmd import WebserverCmd

from ng3.ng3_demo import GraphNavigatorDemoWebserver


class GraphNavigatorCmd(WebserverCmd):
    """
    command line handling for nicegraph demo
    """


def main(argv: list = None):
    """
    main call
    """
    cmd = GraphNavigatorCmd(
        config=GraphNavigatorDemoWebserver.get_config(),
        webserver_cls=GraphNavigatorDemoWebserver,
    )
    exit_code = cmd.cmd_main(argv)
    return exit_code


DEBUG = 0
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())
