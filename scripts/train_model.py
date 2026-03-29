import os
import json
import pickle
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "tamilnadu_government_info.json")
FINE_TUNE_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "tamilnadu_finetune_data.pkl")
MODEL_SAVE_PATH = os.path.join(PROJECT_ROOT, "fine-tuned-tamilnadu-model")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

examples = []

for cm in data["chief_ministers"]:
    q = f"Who was the Chief Minister of Tamil Nadu in {cm['term']}?"
    a = f"{cm['name']} was the Chief Minister during {cm['term']}."
    examples.append(InputExample(texts=[q, a]))

cm = data["current_chief_minister"]
examples.append(InputExample(texts=[
    "Who is the current Chief Minister of Tamil Nadu?",
    f"{cm['name']} is the current CM since {cm['assumed_office']}."
]))

examples.append(InputExample(texts=[
    f"What departments are handled by {cm['name']}?",
    ", ".join(cm['departments'])
]))

gov = data["governor"]
examples.append(InputExample(texts=[
    "Who is the Governor of Tamil Nadu?",
    f"{gov['name']} assumed office on {gov['assumed_office']} and resides at {gov['residence']}."
]))

for minister in data["council_of_ministers"]:
    examples.append(InputExample(texts=[
        f"What departments are handled by {minister['name']}?",
        ", ".join(minister['departments'])
    ]))

for dept in data["departments"]["list"]:
    examples.append(InputExample(texts=[
        f"What is the function of {dept['name']}?",
        dept['functions']
    ]))
    for scheme in dept.get("initiatives", []):
        examples.append(InputExample(texts=[
            f"Name a scheme under {dept['name']}.",
            scheme
        ]))

# Save the data
with open(FINE_TUNE_DATA_PATH, "wb") as f:
    pickle.dump(examples, f)

# Fine-tune the model
model = SentenceTransformer("all-MiniLM-L6-v2")
train_loader = DataLoader(examples, shuffle=True, batch_size=8)
train_loss = losses.MultipleNegativesRankingLoss(model)

model.fit(train_objectives=[(train_loader, train_loss)], epochs=2, warmup_steps=10)
model.save(MODEL_SAVE_PATH)