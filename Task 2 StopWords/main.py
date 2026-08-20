from pathlib import Path

import nltk
from nltk.corpus import stopwords
from transformers import pipeline

TASKS_DIR = Path(__file__).parents[1]
NLTK_DATA_DIR = TASKS_DIR / "nltk_data"
if str(NLTK_DATA_DIR) not in nltk.data.path:
    nltk.data.path.insert(0, str(NLTK_DATA_DIR))

sentences_file = Path(__file__).parent / "data" / "sentences.txt"
sentences = [line.strip() for line in sentences_file.read_text(encoding="utf-8").splitlines() if line.strip()]
stop_words = set(stopwords.words("english"))
sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
flipped_sentences = []

print("Sentence | Original Sentiment | Original Score | Filtered Sentiment | Filtered Score | Result")
print("-" * 120)

for sentence in sentences:
    filtered = " ".join(word for word in sentence.split() if word.lower().strip(".,!?;:") not in stop_words)
    original = sentiment(sentence)[0]
    filtered_result = sentiment(filtered)[0]
    result = "FLIPPED" if original["label"] != filtered_result["label"] else "SAME"
    if result == "FLIPPED":
        flipped_sentences.append((sentence, original, filtered_result))
    print(f"{sentence} | {original['label']} | {original['score']:.3f} | {filtered_result['label']} | {filtered_result['score']:.3f} | {result}")
    print(f"Filtered: {filtered}")

print("\nExplanation:")
if flipped_sentences:
    for sentence, original, filtered_result in flipped_sentences:
        removed = [word.strip(".,!?;:") for word in sentence.split() if word.lower().strip(".,!?;:") in stop_words]
        print(f"Polarity flipped in '{sentence}' because removing {', '.join(removed)} changed the model label from {original['label']} to {filtered_result['label']}.")
else:
    print("No sentence changed the Transformer model label after stop-word removal.")
