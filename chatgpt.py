import openai
from utils import *

class ChatGPT(object):

    def __init__(self, api_key:str) -> None:
        self.messages = []
        self.tokens = 0
        self.cost = 0
        openai.api_key = api_key

    def init_conversation(self, system_setting: str = None) -> None:
        if system_setting is None:
            system_setting = "You are an teaching assistant whose primary responsibilities include \
                telling me related topic notes or background knowledge about a AP calculus math question. \
                It is essential that you strive for accuracy and precision in your work to \
                ensure that the information you provide is as reliable and informative as possible."

        self.messages = []
        self.messages.append({"role": "system", "content": system_setting})

    def continue_conversation(self,
                              question: str,
                              length: str = "4k",
                              temperature: float = 0.2,
                              url: str = "") -> str:
        assert length in ["4k", "16k"]
        if length == "4k":
            model_name = "gpt-3.5-turbo"
        elif length == "16k":
            model_name = "gpt-3.5-turbo-16k"

        self.messages.append({"role": "user", "content": question})
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=self.messages,
                    temperature=temperature,
                )
                break
            except Exception as e:
                if any(i in str(e) for i in [
                        "That model is currently overloaded with other requests.",
                        "The server is overloaded or not ready yet.",
                        "The server had an error while processing your request.",
                        "Bad gateway.",
                ]):
                    if url != "":
                        print_log(
                            "Url: %s, OpenAI api gets error, retry..."
                            % url,
                            mode="warning")
                    else:
                        print_log(
                            "OpenAI model is currently overloaded, retry...",
                            mode="warning")
                    continue
                elif any(i in str(e) for i in [
                    "This key is associated with a deactivated account. If you feel this is an error, contact us through our help center at help.openai.com.",
                    "Incorrect API key provided",
                    "Your account is not active, please check your billing details on our website."
                ]):
                    print("key invalid")
                    raise e
                else:
                    print("==",e,"==")
                    raise e
        if length == "4k":
            in_price = 0.0015 / 1000
            out_price = 0.002 / 1000
        else:
            in_price = 0.003 / 1000
            out_price = 0.004 / 1000
        self.cost += response["usage"]["prompt_tokens"] * in_price + response[
            "usage"]["completion_tokens"] * out_price
        self.tokens += response["usage"]["total_tokens"]
        answer = response["choices"][0]["message"]["content"]
        if "Invalid condensations" in answer:
            raise Exception("Invalid condensations")
        self.messages.append({"role": "assistant", "content": answer})
        return answer
