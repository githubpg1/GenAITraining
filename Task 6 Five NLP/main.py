import re
from collections import Counter
from pathlib import Path

from transformers import pipeline

DATA_FILE = Path(__file__).parent / "data" / "sdlc_qa_texts.txt"
texts = [line.strip() for line in DATA_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]

pos_tagger = pipeline("token-classification", model="vblagoje/bert-english-uncased-finetuned-pos", aggregation_strategy="simple")
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")
sentiment = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

for number, text in enumerate(texts, 1):
    words = re.findall(r"[a-z]+", text.lower())
    print("\n" + "=" * 60)
    print(f"TEXT {number}")
    print("=" * 60)
    print(f"\nOriginal Text:\n{text}")

    print("\n--- POS ---")
    for item in pos_tagger(text)[:8]:
        print(f"{item['word']} -> {item['entity_group']}")

    print("\n--- NER ---")
    entities = ner(text)
    if entities:
        for item in entities:
            print(f"{item['word']} -> {item['entity_group']}")
    else:
        print("No named entities detected.")

    print("\n--- CLASSIFICATION ---")
    candidate_labels = ["requirement", "testing", "defect", "release", "governance"]
    classification = classifier(text, candidate_labels)
    category = classification["labels"][0]
    score = classification["scores"][0]
    print(f"Category: {category.upper()}")
    print(f"Confidence: {score:.3f}")
    print("Reason: the Transformer selected this category from the meaning of the text.")

    print("\n--- SENTIMENT ---")
    result = sentiment(text)[0]
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.3f}")

    print("\n--- N-GRAMS ---")
    print("Unigrams:", ", ".join(word for word, _ in Counter(words).most_common(8)))
    print("Bigrams:", ", ".join(" ".join(pair) for pair, _ in Counter(zip(words, words[1:])).most_common(5)))
    print("Trigrams:", ", ".join(" ".join(triple) for triple, _ in Counter(zip(words, words[1:], words[2:])).most_common(5)))

print("""
============================================================
SUMMARY
============================================================
POS:
Definition: POS tagging assigns grammatical labels such as noun or verb to words.
Why we need it: It helps QA systems understand actions, objects, and requirements.

NER:
Definition: NER finds named entities such as systems, products, people, or dates.
Why we need it: It helps extract release, tool, team, and environment references.

Classification:
Definition: Classification assigns text to a meaningful category using evidence.
Why we need it: It routes requirements, defects, testing, and release information.

Sentiment:
Definition: Sentiment analysis predicts the positive or negative tone of text.
Why we need it: It can highlight frustration, confidence, or delivery-risk signals.

N-Grams:
Definition: N-Grams are sequences of one, two, or three neighboring words.
Why we need it: They reveal recurring QA terminology and useful phrases.

These techniques are part of Natural Language Processing (NLP), which processes
human language. AI/ML models learn or infer patterns, while Agentic AI uses models,
context, tools, reasoning, and actions to achieve goals. NLP is not itself an agent.

Most useful NLP task for SDLC-QA: Classification.
Why: Classification can route each item to the correct governance workflow, such as
requirements review, defect triage, testing analysis, or release approval. In a real
SDLC-QA agent, all five techniques complement one another rather than replace one task.

============================================================
AGENTIC AI CONNECTION
============================================================
POS and NER extract language details, classification identifies the work type,
sentiment detects tone or risk signals, and N-Grams find recurring terminology.
An SDLC-QA agent can use these outputs for retrieval, reasoning, reporting, and action.
""")
