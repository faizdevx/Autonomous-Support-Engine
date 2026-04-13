from transformers import pipeline

generator = pipeline("text-generation", model="google/flan-t5-base")

def call_llm(prompt):
    return generator(prompt, max_length=200)[0]['generated_text']