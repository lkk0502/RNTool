import os
import traceback


class Tools:

    @staticmethod
    def checkdir(path: str):
        """檢查目錄是否存在，否則建立."""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                traceback.print_exc()
