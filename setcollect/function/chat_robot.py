from django.shortcuts import render, redirect, HttpResponse
from llmtuner import ChatModel
from llmtuner.hparams import (
    ModelArguments, 
    FinetuningArguments, 
    DataArguments, 
    GeneratingArguments
)

http_address = "http://127.0.0.1:8000/"

def chatbot_view(request):
    return render(request, 'chat_bot.html')

def chat_bot_response(request):
    opening_message = ""
    
    if request.method == "POST":
        
        ##########get userInput from front##############
        query = request.body.decode('utf-8')
        print(query)
        
        if query == "clear":
            history = []
            print("History has been removed.")
            return redirect(http_address + "chatbot/")
        
        
        ############init args for the model############
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
            temperature=0.90,
            max_new_tokens=512,
            top_p=0.7,
            repetition_penalty=1.02,
        )
        chat_model = ChatModel(
            model_args=model_args,
            data_args=data_args,
            finetuning_args=finetuning_args,
            generating_args=generating_arguments,
        )
        ###############################################

        ###########init an empty history list##########        
        history = []
        response = ""
            
        while True:
            if query == "exit":
                break


            for new_text in chat_model.stream_chat(query, history):
                response += new_text
            
            history = history + [(query, response)]
        
            return HttpResponse(response)
        
    ### return an error response for non-POST requests
    return HttpResponse(status=400) 

        
        
        
        
        
def chat_eval(request):
    return
    