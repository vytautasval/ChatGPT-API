import openai
import sys
import tiktoken
import os

def main():
    if len(sys.argv) != 2:
        print("AI needs a name!")
        sys.exit()

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    print(os.environ.get("OPENAI_API_KEY"))
    chat_log = None
    total_tokens = []

    while True:
        try:
            user_msg = input("User: ")
            info = chat(user_msg, chat_log)
            answer = info[0]
            chat_log = info[1]
            total_tokens = token_counter(answer, total_tokens)
            print("AI: ", answer)
        except EOFError:
            print("Bye!")
            print("Tokens used:", sum(total_tokens))
            sys.exit()


def chat(user_msg, chat_log):
    system_msg = f"You are a positive and helpful jokester. Your name is {sys.argv[1]}."

    if chat_log is None:
        chat_log = [
            {"role": "system", "content": system_msg},
        ]
    chat_log.append({"role": "user", "content": user_msg})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chat_log, max_tokens=100)

    answer = response["choices"][0]["message"]["content"]

    chat_log.append({"role": "assistant", "content": answer})
    info = [answer, chat_log]
    return info


def token_counter(answer, total_tokens):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(answer))
    total_tokens.append(num_tokens)

    return total_tokens

if __name__ == "__main__":
    main()
