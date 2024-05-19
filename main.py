import logs
import logging
import os
from typing import List

from openai import ChatCompletion, OpenAI

from commands import movement_commands
from dionysus.command.descriptor import CommandDescriptor
from dionysus.parser import ChatResultParser
from dionysus.prompt_template import PromptTemplate
from image import set_user_message

robot_controller_prompt = PromptTemplate(
    identity="""You control a robot dog. You will be provided with images taken from the onboard camers. The images will be ordered left, and forward views. Choose the next best action given your goal and the environment. If there is an obstacle in the way, rotate until it's no longer in the way or move backwards.""",
    command_set=movement_commands
)

parser = ChatResultParser(movement_commands)

last_actions = []


def get_next_actions(forward_view_image_paths: List[str], goal: str) -> List[CommandDescriptor]:
    """Get and rune the next action to take based on the current view of the environment."""
    global last_actions

    # load the image from "current_view.png" and pass it to the model along with the system prompt
    user_messages = [set_user_message(goal, file_path_list=[forward_view_image_path], max_size_px=200, tiled=True) for forward_view_image_path in forward_view_image_paths]

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion: ChatCompletion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": robot_controller_prompt.as_system_message()},
            # up to 10 previous actions
            *last_actions[-10:],
            *[u[0] for u in user_messages]
        ],
        model="gpt-4-turbo",
    )

    llm_response = chat_completion.choices[0].message.content

    # add the last actions to
    last_actions.extend([{
        "role": "user",
        "content": "Which actions should you take? <image omitted for context>"
    }, {
        "role": "assistant",
        "content": llm_response
    }])

    logging.info(f"Full LLM Response\n\n{llm_response}")

    return parser(llm_response)


def get_next_picture() -> List[str]:
    # TODO: get the next picture from the dog's camera
    return [
        "canvas_image_0.png",
        "canvas_image_1.png",
        # "canvas_image_3.png",
        # "canvas_image_4.png",
        # "canvas_image_5.png",
    ]


def run():
    # TODO: run this in a loop
    goal = "Find the blue recycle bin, face it, and walk up to it. Do not repeat the same action many times if you are stuck. If there is an obstacle in the way, rotate or move backwards."

    while True:
        try:
            live_view = get_next_picture()
            
            logging.info("Getting next actions")
            
            actions: List[CommandDescriptor] = get_next_actions(forward_view_image_paths=live_view, goal=goal)

            logging.info("Taking actions")

            for action in actions:
                for result in action.execute():
                    if isinstance(result, dict) and "object_name" in result and len(actions) == 1:
                        logging.info(f"Found object {result['object_name']} at location {result['object_location']}")
                        break
        except Exception as e:
            logging.exception(e)
            logging.error("An error occurred while processing the next action. Trying again")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.exception(e)
        exit(1)
    except KeyboardInterrupt:
        logging.info("Exiting...")
        exit(0)