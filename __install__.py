from streamcontroller_plugin_tools.installation_helpers import create_venv
from os.path import join, abspath, dirname

toplevel = dirname(abspath(__file__))
create_venv(join(toplevel, "VTubeStudio", ".venv"), join(toplevel, "VTubeStudio", "requirements.txt"))
