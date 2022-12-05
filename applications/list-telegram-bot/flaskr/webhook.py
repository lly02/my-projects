import re

from . import command


class Webhook(object):
    """
    To receive incoming data using webhook.
    """
    def __init__(self):
        self.state = {
            "command": "",
            "step": 0,
            "data": {},
            "error": "",
            "result": {}
        }
        self.command = command.Command()

    def is_command(self, result):
        """
        Validate if the message sent is a command / in the middle of a command.
        """
        self.state["result"] = result

        # New command
        if "message" in self.state["result"] and self.state["result"]["message"]["chat"]["type"] == "group":
            if self.state["command"] != "":
                self.state["data"]["text"] = result["message"]["text"]
                self.process_command(self.state["command"])
            elif self.state["result"]["message"]["text"][0] == "/":
                self.process_command(result["message"]["text"])

        # Middle of a command
        elif ("callback_query" in self.state["result"] and
              self.state["result"]["callback_query"]["message"]["chat"]["type"] == "group"):
            if self.state["command"] != "":
                self.state["data"]["text"] = result["callback_query"]["data"]
                self.process_command(self.state["command"])
            elif self.state["result"]["callback_query"]["data"][0] == "/":
                self.process_command(self.state["result"]["callback_query"]["data"])

    def process_command(self, message):
        """
        Process the command and execute the necessary methods.

        :param message: The actual message (command) sent by the user
        """
        if "text" in self.state["data"] and self.state["data"]["text"] == "done":
            self.state = self.command.start()
        elif re.search(r"^/help\w*$", message):
            self.state = self.command.start()
        elif re.search(r"^/start\w*$", message):
            self.state = self.command.start()
        elif re.search(r"^/display\w*$", message):
            self.state = self.command.display_schedule(self.state)
        elif re.search(r"^/add\w*$", message):
            self.state = self.command.add_schedule(self.state)
        # elif re.search(r"^/update\w*$", message):
        #     self.state = self.command.update_schedule(self.state)
        elif re.search(r"^/del\w*$", message):
            self.state = self.command.delete_schedule(self.state)
