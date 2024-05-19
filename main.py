import logging
from typing import List
from dionysus.command.descriptor import CommandDescriptor
import logs
import os
from commands import movement_commands
from dionysus.parser import ChatResultParser
from dionysus.prompt_template import PromptTemplate
from openai import ChatCompletion, OpenAI
from image import set_user_message

robot_controller_prompt = PromptTemplate(
    identity="""You control a robot dog. You will be provided with an image taken from a forward looking camera. You choose what the next best action is.""",
    command_set=movement_commands
)

parser = ChatResultParser(movement_commands)


def get_next_actions(forward_view_image_paths: List[str], goal: str) -> List[CommandDescriptor]:
    """Get and rune the next action to take based on the current view of the environment."""

    # load the image from "current_view.png" and pass it to the model along with the system prompt
    user_messages = [set_user_message(goal, file_path_list=[forward_view_image_path], max_size_px=5, tiled=True) for forward_view_image_path in forward_view_image_paths]

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion: ChatCompletion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": robot_controller_prompt.as_system_message()},
            *[u[0] for u in user_messages]
        ],
        model="gpt-4o",
    )

    llm_response = chat_completion.choices[0].message.content

    logging.info(f"Full LLM Response\n\n{llm_response}")

    return parser(llm_response)


def get_next_picture() -> str:
    # TODO: get the next picture from the dog's camera
    return "current_view.png"


def run():
    # TODO: run this in a loop
    goal = "Find the red ball."

    while True:
        live_view = get_next_picture()
        actions: List[CommandDescriptor] = get_next_actions(forward_view_image_paths=[live_view], goal=goal)

        for action in actions:
            for result in action.execute():
                if isinstance(result, dict) and "object_name" in result:
                    logging.info(f"Found object {result['object_name']} at location {result['object_location']}")
                    exit(0)


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.exception(e)
        exit(1)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        exit(0)