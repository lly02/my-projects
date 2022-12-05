import requests
import datetime
import re

from . import bot_token, db


class Command(object):
    def __init__(self):
        self.chat_id = "-605130156"
        self.bot_token = bot_token.bot_token
        self.url = f"https://api.telegram.org/bot{self.bot_token}"

    def start(self):
        """
        Starts the bot up with some commands available for user to select.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": "*COMMANDS*\n"
                    "\/display \- Display all added schedules\n"
                    "\/add \- Add a new schedule\n",
            "parse_mode": "MarkdownV2",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "Display schedules",
                            "callback_data": "/display"
                        }
                    ],
                    [
                        {
                            "text": "Add schedule",
                            "callback_data": "/add"
                        }
                    ]
                ]
            }
        }
        r = requests.post(f"{self.url}/sendMessage", json=payload)
        return self.state_reset()

    def display_schedule(self, state):
        """
        A method to gather information from user about displaying schedules.

        :param state: Current state of the information gathering
        :return: Returns the next state
        """
        def post_request(post_payload):
            post_res = requests.post(f"{self.url}/sendMessage", json=post_payload)
            return post_res.json()

        def post_request_edit(post_payload):
            post_res = requests.post(f"{self.url}/editMessageText", json=post_payload)
            return post_res.json()

        # 1. Retrieve all schedule, select a category and set command to /display
        if state["step"] == 0:
            state["command"] = "/display"
            if "message_id" not in state["data"]:
                state["data"]["all_schedules"] = db.get_all_schedule()

            categories = {}
            for data in state["data"]["all_schedules"]:
                categories[data[4]] = None

            state["data"]["selections"] = []
            for category in categories:
                state["data"]["selections"].append([{
                    "text": category,
                    "callback_data": category
                }])
            state["data"]["selections"].append([{
                "text": "-- Done --",
                "callback_data": "done"
            }])

            if "message_id" in state["data"]:
                payload = {
                    "chat_id": self.chat_id,
                    "text": "Select a category.",
                    "message_id": state["data"]["message_id"],
                    "reply_markup": {
                        "inline_keyboard": state["data"]["selections"]
                    }
                }
                res = post_request_edit(payload)
            else:
                payload = {
                    "chat_id": self.chat_id,
                    "text": "Select a category.",
                    "reply_markup": {
                        "inline_keyboard": state["data"]["selections"]
                    }
                }
                res = post_request(payload)

            state["data"]["message_id"] = res["result"]["message_id"]
            state["step"] += 1

            return state

        # 2. Retrieve and display all the schedules according to category selected
        if state["step"] == 1:
            selection = []
            for item in state["data"]["all_schedules"]:
                if item[4] == state["data"]["text"]:
                    selection.append([{
                        "text": item[1],
                        "callback_data": item[0]
                    }])
            selection.append([{
                "text": "<- Back",
                "callback_data": "back"
            }])
            selection.append([{
                "text": "-- Done --",
                        "callback_data": "done"
            }])

            payload = {
                "chat_id": self.chat_id,
                "text": "Select a schedule for more information.",
                "message_id": state["data"]["message_id"],
                "reply_markup": {
                    "inline_keyboard": selection
                }
            }
            res = post_request_edit(payload)
            state["step"] += 1

            return state

        # 3. If "back" is clicked, go back to category selection.
        #    Else show more information of the clicked item
        if state["step"] == 2:
            if state["data"]["text"] == "back":
                state["step"] = 0
                self.display_schedule(state)
                return state
            elif (state["data"]["text"]).isdigit():
                res = db.get_schedule(state["data"]["text"])
                state["data"]["current_schedule"] = res
                payload = {
                    "chat_id": self.chat_id,
                    "text": f"Name: {res[1]}\n"
                            f"Date: {res[3]}\n"
                            f"Category: {res[4]}\n"
                            f"\n{res[2]}\n",
                    "message_id": state["data"]["message_id"],
                    "reply_markup": {
                        "inline_keyboard": [
                            # [
                            #     {
                            #         "text": "Update",
                            #         "callback_data": f"update {res[0]}"
                            #     }
                            # ],
                            [
                                {
                                    "text": "Delete",
                                    "callback_data": f"del {res[0]}"
                                }
                            ],
                            [
                                {
                                    "text": "<- Back",
                                    "callback_data": f"back"
                                }
                            ],
                            [
                                {
                                    "text": "-- Done --",
                                    "callback_data": f"done"
                                }
                            ],
                        ]
                    }
                }
                r = post_request_edit(payload)

                return state
            else:
                state["command"] = ""
                state["step"] = 0
                state["error"] = ""

                # if re.search(r"^update\w*$", state["result"]["message"]["text"]):
                #     state = self.update_schedule(state)
                if re.search(r"^del\w*$", state["data"]["text"]):
                    state = self.delete_schedule(state)

                return state

    def add_schedule(self, state):
        """
        A method to gather information from user about adding schedule.

        :param state: Current state of the information gathering
        :return: Returns the next state
        """
        def post_request(post_payload):
            r = requests.post(f"{self.url}/sendMessage", json=post_payload)
            return r.json()

        def post_request_edit(post_payload):
            r = requests.post(f"{self.url}/editMessageText", json=post_payload)
            return r.json()

        # 1. Ask for name of activity and set command to /add
        if state["step"] == 0:
            state["command"] = "/add"
            payload = {
                "text": f"[1/4] Name of the activity.",
                "chat_id": self.chat_id,
            }
            post_request(payload)
            state["step"] += 1

        # 2. Collect result for name and ask for link
        elif state["step"] == 1:
            state["data"]["add_schedule"] = [state["data"]["text"]]
            payload = {
                "text": f"[2/4] Link of the activity.",
                "chat_id": self.chat_id,
            }
            post_request(payload)
            state["step"] += 1

        # 3. Collect result for link and ask for date
        elif state["step"] == 2:
            state["data"]["add_schedule"].append(state["data"]["text"])
            payload = {
                "text": f"[3/4] Date of the activity.",
                "chat_id": self.chat_id,
            }
            post_request(payload)
            state["step"] += 1

        # 4. Collect result for date and ask for category
        elif state["step"] == 3:
            state["data"]["add_schedule"].append(state["data"]["text"])
            all_schedules = db.get_all_schedule()

            categories = {}
            for data in all_schedules:
                categories[data[4]] = None

            selection = []
            for category in categories:
                selection.append([{
                    "text": category,
                    "callback_data": category
                }])

            payload = {
                "text": f"[4/4] Category of the activity. Enter new name to add category.",
                "chat_id": self.chat_id,
                "reply_markup": {
                    "inline_keyboard": selection
                }
            }
            res = post_request(payload)
            print(selection)
            state["step"] += 1

        # 5. Collect result for category and add record into DB
        elif state["step"] == 4:
            if state["error"] == "":
                state["data"]["add_schedule"].append(state["data"]["text"])
                payload = {
                    "text": f"Adding schedule...",
                    "chat_id": self.chat_id,
                }
                res = post_request(payload)
                db.insert_schedule(state["data"]["add_schedule"])

                state["step"] += 1
                payload = {
                    "text": f"Schedule added.",
                    "message_id": res["result"]["message_id"],
                    "chat_id": self.chat_id,
                    "reply_markup": {
                        "inline_keyboard": [[{
                            "text": "-- Done --",
                            "callback_data": "done"
                        }]]
                    }
                }
                post_request_edit(payload)
                state = self.state_reset()
            else:
                post_request(state["error"])

        return state

    def update_schedule(self, state):
        """
        A method to gather information from user about updating schedule.

        :param state: Current state of the information gathering
        :return: Returns the next state
        """
        pass

    def delete_schedule(self, state):
        """
        A method to gather information from user about deleting schedule.

        :param state: Current state of the information gathering
        :return: Returns the next state
        """
        def post_request_edit(post_payload):
            post_res = requests.post(f"{self.url}/editMessageText", json=post_payload)
            return post_res.json()

        if state["step"] == 0:
            state["command"] = "/del"

            payload = {
                "chat_id": self.chat_id,
                "text": "Confirm schedule delete.",
                "message_id": state["data"]["message_id"],
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Yes",
                                "callback_data": "delete"
                            }
                        ],
                        [
                            {
                                "text": "No",
                                "callback_data": "done"
                            }
                        ]
                    ]
                }
            }
            res = post_request_edit(payload)
            state["step"] += 1

        if state["step"] == 1:
            if state["data"]["text"] == "delete":
                db.delete_schedule(state["data"]["current_schedule"][0])

                payload = {
                    "chat_id": self.chat_id,
                    "text": "Schedule deleted.",
                    "message_id": state["data"]["message_id"],
                    "reply_markup": {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "-- Done --",
                                    "callback_data": "done"
                                }
                            ],
                        ]
                    }
                }
                r = post_request_edit(payload)

        return state

    @staticmethod
    def input_sanitize(user_input, check_type):
        """
        Sanitize user input.

        :param user_input: User input
        :param check_type: The type of input user given
        :return: Returns error message else None
        """
        err_msg = None
        if check_type == "date":
            if len(user_input) != 6:
                err_msg = "Please enter date in the format DDMMYY."
            elif int(user_input[0] + user_input[1]) > 31:
                err_msg = "DD should be < 31"
            elif int(user_input[0] + user_input[1]) == 0:
                err_msg = "DD should be > 0"
            elif int(user_input[2] + user_input[3]) > 12:
                err_msg = "MM should be < 31"
            elif int(user_input[2] + user_input[3]) == 0:
                err_msg = "MM should be > 0"
            elif int("20" + user_input[4] + user_input[5]) - datetime.date.today().year < 0:
                err_msg = "YY should not be before this year."
            elif int(user_input[2] + user_input[3]) - datetime.date.today().month < 0:
                err_msg = "MM should not be before this month."
            elif int(user_input[0] + user_input[1]) - datetime.date.today().day < 0:
                err_msg = "DD should not be before today."

        return err_msg

    @staticmethod
    def state_reset():
        """
        Return default state values for reset.
        """
        return {
            "command": "",
            "step": 0,
            "data": {},
            "error": "",
            "result": {}
        }
