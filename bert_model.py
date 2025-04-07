import streamlit as st
import html
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers.pipelines.token_classification import TokenClassificationPipeline

model_path = r"D:\Users\alina\rrrr\truth_of_the_matter_model_rubert_tiny2"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

class CustomTokenClassificationPipe(TokenClassificationPipeline):
    def preprocess(self, sentence, offset_mapping=None, **preprocess_params):
        encoded_data = self.tokenizer(
            sentence,
            return_tensors="pt",
            truncation=True,
            return_special_tokens_mask=True,
            return_offsets_mapping=True,
            return_overflowing_tokens=True,
            max_length=self.tokenizer.model_max_length,
            padding=True
        )

        chunk_count = len(encoded_data["input_ids"])

        for i in range(chunk_count):
            inputs = {k: v[i].unsqueeze(0) for k, v in encoded_data.items()}
            inputs["sentence"] = sentence if i == 0 else None
            inputs["is_last"] = (i == chunk_count - 1)

            yield inputs

    def _forward(self, inputs):
        offset_mapping = inputs.pop("offset_mapping", None)

        special_tokens_mask = inputs.pop("special_tokens_mask")
        sentence = inputs.pop("sentence")
        is_last = inputs.pop("is_last")

        overflow_to_sample_mapping = inputs.pop("overflow_to_sample_mapping")

        output = self.model(**inputs)
        logits = output["logits"] if isinstance(output, dict) else output[0]

        output_data = {
            "offset_mapping": offset_mapping,
            "logits": logits,
            "special_tokens_mask": special_tokens_mask,
            "sentence": sentence,
            "overflow_to_sample_mapping": overflow_to_sample_mapping,
            "is_last": is_last,
            **inputs,
        }
        output_data["input_ids"] = output_data["input_ids"].reshape(1, -1)
        output_data["token_type_ids"] = output_data["token_type_ids"].reshape(1, -1)
        output_data["attention_mask"] = output_data["attention_mask"].reshape(1, -1)
        output_data["special_tokens_mask"] = output_data["special_tokens_mask"].reshape(1, -1)
        output_data["offset_mapping"] = output_data["offset_mapping"].reshape(1, -1, 2)

        return output_data

LABELS = ['O', 'B-DATE', 'B-LAW', 'B-MONEY', 'B-PER', 'B-REGION']

def predict(text_input):
    model.config.id2label = dict(enumerate(LABELS))
    model.config.label2id = {v: k for k, v in model.config.id2label.items()}

    predictions_pipeline = CustomTokenClassificationPipe(model=model, tokenizer=tokenizer, aggregation_strategy='max')

    return predictions_pipeline(text_input)

color_mapping = {
    "DATE": "#34C924", 
    "LAW": "#333FFF", 
    "MONEY": "red", 
    "PER": "orange", 
    "REGION": "#F754E1"
}
label_mapping = {
    "DATE": "Date", 
    "LAW": "Law", 
    "MONEY": "Money", 
    "PER": "Person", 
    "REGION": "Region"
}
def process_and_display(text_input):
    
    prediction_results = predict(text_input)
       
    rendered_parts = []
    previous_end = 0
    marked_indices = []

    for prediction in prediction_results:
        start_index = prediction['start']
        end_index = prediction['end']
        entity_type = prediction['entity_group']
        token = html.escape(text_input[start_index:end_index])
        
        overlaps = any(start_index < end_idx and end_index > start_idx for start_idx, end_idx in marked_indices)

        if not overlaps:
            marked_indices.append((start_index, end_index))
            color_code = color_mapping.get(entity_type, "black")
            highlighted_text = f'<span style="color:{color_code};">{token}</span>'
            rendered_parts.append(text_input[previous_end:start_index])
            rendered_parts.append(highlighted_text)
            previous_end = end_index
            
    rendered_parts.append(text_input[previous_end:])
    html_rendered = ''.join(rendered_parts)
    
    legend_rendered = []
    for entity, color_code in color_mapping.items():
        label = label_mapping.get(entity, entity)
        legend_rendered.append(f'<span style="color:{color_code};">{entity} - {label}</span>')
    
    st.markdown('&nbsp; | &nbsp;'.join(legend_rendered), unsafe_allow_html=True)
    st.markdown(html_rendered, unsafe_allow_html=True)
