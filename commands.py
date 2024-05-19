import logging
from time import sleep
from typing import List
from dionysus.argument.base import Argument
from dionysus.argument_type.primative import String
from dionysus.command.base import Command
from dionysus.commandset import CommandSet
import requests

def get(path: str):
    requests.get(f"http://localhost:3012/api/{path}")
    sleep(1)


class MoveRobot(Command):
    arguments: List[Argument] = [
        Argument("direction", String(), choices=["forward", "forward-long", "backward"]),
        Argument("reason", String())
    ]

    def run(self, command_args, *args, **kwargs):
        # TODO: send the command to the robot
        get(command_args['direction'])
        logging.info(f"Moving robot {command_args['direction']}. Reason={command_args['reason']}")


class RotateRobot(Command):
    arguments: List[Argument] = [
        Argument("direction", String(), choices=["left"]),
        Argument("reason", String())
    ]

    def run(self, command_args, *args, **kwargs):
        # TODO: send the command to the robot
        if (command_args['direction'] == "right"):
            return
        get(command_args['direction'])
        logging.warn(f"Rotating robot {command_args['direction']}. Reason={command_args['reason']}")


class FoundObject(Command):
    """When you find the object, you can run this command to log the object location."""

    arguments: List[Argument] = [
        Argument("object_name", String()),
        Argument("object_location", String())
    ]

    def run(self, command_args, *args, **kwargs):
        # get("dance")
        logging.warn(f"Found object {command_args['object_name']} at location {command_args['object_location']}")

        yield {"object_name": command_args["object_name"], "object_location": command_args["object_location"]}


movement_commands = CommandSet.from_definitions([MoveRobot, RotateRobot, FoundObject])