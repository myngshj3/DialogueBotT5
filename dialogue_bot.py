import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import T5ForConditionalGeneration, T5Tokenizer


class DialogueBot:

    def __init__(self):
        self._config = None
        self._model = None
        self._tokenizer = None
        self.configure()

    @property
    def config(self):
        return self._config
    
    @property
    def model(self) -> AutoModelForCausalLM:
        return self._model
    
    @property
    def tokenizer(self) -> AutoTokenizer:
        return self._tokenizer

    def configure(self):
        with open("config.json", "r", encoding="utf-8") as f:
            self._config = json.load(f)

    def reconfigure(self):
        self.configure()

    def load_model(self):
        model_name = self._config["model_name"]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        self._tokenizer = tokenizer
        self._model = model
        #self._tokenizer = T5Tokenizer.from_pretrained(model_name)
        #self._model = T5ForConditionalGeneration.from_pretrained(model_name)

    def have_dialogue(self, input_text: str) -> str:
        print("question:", input_text)
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt",
                                          max_length=self._config["max_input_length"], truncation=True)
        output = self.model.generate(input_ids, max_length=self._config["max_input_length"],
                                     num_return_sequences=1, pad_token_id=50256)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        #output = self.model.generate(input_ids,
        #                             max_length=self._config["max_output_length"],
        #                             num_return_sequences=1)
        #response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(response + "\n")
            print("output is written.")
        return response
    
    def console_dialogue_loop(self):
        while True:
            input_text: str = input("Input question:")
            input_utf8: str = input_text.encode(self._config["codec"]).decode("utf-8", errors="replace")
            response_utf8: str = self.have_dialogue(input_utf8)
            response: str = response_utf8.encode("utf-8").decode(self._config["codec"], errors="replace")
            print("output:", response)
