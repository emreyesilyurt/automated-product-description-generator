from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class LLM_Agent:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-neo-125M')
        self.model = AutoModelForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def query_llm(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors='pt', padding=True, truncation=True)
        inputs['attention_mask'] = (inputs['input_ids'] != self.tokenizer.pad_token_id).long()
        outputs = self.model.generate(inputs.input_ids, attention_mask=inputs['attention_mask'], max_length=150)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

class MarketingCheckerAgent:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    def check_for_marketing_qualifiers(self, description):
        result = self.classifier(description)
        for res in result:
            if res['label'] == 'POSITIVE' and res['score'] > 0.8:
                return True
        return False
