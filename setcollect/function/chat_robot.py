from django.shortcuts import render, redirect
from llmtuner import ChatModel
from dataclasses import dataclass
from llmtuner.tuner.core.loader import load_model_and_tokenizer
from llmtuner.hparams import ModelArguments, FinetuningArguments, DataArguments, GeneratingArguments


http_address = "http://127.0.0.1:8000/"


def chat_bot(request):
    if request.method == "GET":
        
        model_args = ModelArguments(
            model_name_or_path="/home/vcp/YiMu/LLaMA-Efficient-Tuning/essay05"
        )
        finetuning_args = FinetuningArguments(
            finetuning_type="lora"
        )
        data_args = DataArguments(
            prompt_template="default"
        )
        generating_arguments = GeneratingArguments(
            temperature=0.1,
            max_new_tokens=512,
            top_p=0.7,
        )
        
        chat_model = ChatModel(
            model_args=model_args,
            data_args=data_args,
            finetuning_args=finetuning_args,
            generating_args=generating_arguments,
        )
        history = []
        
    print("Welcome to the CLI application, use `clear` to remove the history, use `exit` to exit the application.")

    while True:
        try:
            query = input("\nUser: ")
        except UnicodeDecodeError:
            print("Detected decoding error at the inputs, please set the terminal encoding to utf-8.")
            continue
        except Exception:
            raise

        if query.strip() == "exit":
            break

        if query.strip() == "clear":
            history = []
            print("History has been removed.")
            continue

        print("Assistant: ", end="", flush=True)

        response = ""
        for new_text in chat_model.stream_chat(query, history):
            print(new_text, end="", flush=True)
            response += new_text
        print()

        history = history + [(query, response)]
        
        return render(request, "chat_bot.html")
        
    