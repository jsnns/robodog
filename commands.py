import logging
from typing import List
from dionysus.argument.base import Argument
from dionysus.argument_type.primative import String
from dionysus.command.base import Command
from dionysus.commandset import CommandSet


class MoveRobot(Command):
    arguments: List[Argument] = [
        Argument("direction", String(), choices=["forward", "backward"]),
        Argument("reason", String())
    ]

    def run(self, command_args, *args, **kwargs):
        # TODO: send the command to the robot
        logging.info(f"Moving robot {command_args['direction']}. Reason={command_args['reason']}")


class RotateRobot(Command):
    arguments: List[Argument] = [
        Argument("direction", String(), choices=["clockwise", "counter-clockwise"]),
        Argument("reason", String())
    ]

    def run(self, command_args, *args, **kwargs):
        # TODO: send the command to the robot
        logging.warn(f"Rotating robot {command_args['direction']}. Reason={command_args['reason']}")


class FoundObject(Command):
    """When you find the object, you can run this command to log the object location."""

    arguments: List[Argument] = [
        Argument("object_name", String()),
        Argument("object_location", String())
    ]

    def run(self, command_args, *args, **kwargs):
        logging.warn(f"Found object {command_args['object_name']} at location {command_args['object_location']}")

        yield {"object_name": command_args["object_name"], "object_location": command_args["object_location"]}


movement_commands = CommandSet.from_definitions([MoveRobot, RotateRobot, FoundObject])