from lux.setup.launch_window import LaunchWindow
from lux.setup.lux_window import LuxWindow
from lux.get_window import set_window
from lux.setup.logging import setup_logging
from lux.data import get_config


def launch():
    setup_logging()

    # try:
    #     launch_cfg = get_config("launch")
    # except Exception as e:
    #     print(e)
    #     launch_window = LaunchWindow()
    #     launch_window.run()
    #     # launch_cfg = get_config("launch")  -- TODO

    lux_window = LuxWindow()
    set_window(lux_window)
    lux_window.run()


