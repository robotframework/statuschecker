from robot.api import logger


class MyLib:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def add(self, a: int, b: int) -> int:
        print(f"Adding {a} and {b}")
        return a + b

    def _end_test(self, name, attrs):
        logger.info(f"Test {name} ended with {attrs}")
