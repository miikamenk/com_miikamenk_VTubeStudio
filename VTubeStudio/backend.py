from streamcontroller_plugin_tools import BackendBase
import os
import rpyc
import subprocess
import time
from loguru import logger as log
import atexit

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.conn = None
        venv_python = os.path.join(
            os.path.dirname(__file__),
            ".venv", "bin", "python"
        )

        server_script = os.path.join(
            os.path.dirname(__file__),
            "vts_rpc_server.py"
        )

        self.server_process = subprocess.Popen(
            [venv_python, server_script],
            cwd=os.path.dirname(__file__)
        )
        ## time.sleep(5)
        ## self.conn = rpyc.connect("localhost", 18812) 
        self.conn = self._wait_for_server(10)
        atexit.register(self.shutdown)

    def _wait_for_server(self, timeout=5):
        """Wait for the server to be up before attempting to connect."""
        start_time = time.time()
        last_exception = None
        while time.time() - start_time < timeout:
            try:
                conn = rpyc.connect("localhost", 18812)
                log.info("Server is up and ready to accept connections.")
                return conn
            except Exception as e:
                last_exception = e
                time.sleep(0.5)  # Retry after a short delay
        raise TimeoutError(f"Failed to connect to the server within {timeout} seconds. Last error: {last_exception}")

    def get_connected(self):
        return self.conn.root.get_connected()

    def connect_auth(self):
        return self.conn.root.connect_auth()

    def getHotkeys(self)->list[str]:
        return self.conn.root.get_hotkeys()

    def triggerHotkey(self, hotkey: str)->bool:
        return self.conn.root.trigger_hotkey(hotkey)

    def moveModel(self, x: float, y: float, rot: int, size: int, relative: bool, move_time: float)->bool:
        return self.conn.root.move_model(x, y, rot, size, relative, move_time)

    def getModelPosition(self):
        return self.conn.root.get_model_postion()

    def shutdown(self):
        if self.server_process:
            log.info("Shutting down VTS RPyC server...")
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            log.info("VTS RPyC server shut down.")

backend = Backend()

