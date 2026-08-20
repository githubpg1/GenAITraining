import re
from pathlib import Path

import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

TASKS_DIR = Path(__file__).parents[1]
NLTK_DATA_DIR = TASKS_DIR / "nltk_data"
if str(NLTK_DATA_DIR) not in nltk.data.path:
    nltk.data.path.insert(0, str(NLTK_DATA_DIR))

DATA_FILE = Path(__file__).parent / "data" / "sdlc_qa_messy_texts.txt"
texts = [line.strip() for line in DATA_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
lemmatizer = WordNetLemmatizer()
domain_terms = {
    "requirement", "user", "story", "acceptance", "criteria", "qa", "test",
    "testing", "defect", "bug", "regression", "coverage", "traceability",
    "release", "deployment", "production", "approval"
}

clean_texts = [
    " ".join(re.findall(r"[a-z]+", re.sub(r"https?://\S+|\S+@\S+", " ", text.lower())))
    for text in texts
]
vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b[a-z]+\b")
tfidf = vectorizer.fit_transform(clean_texts)
terms = vectorizer.get_feature_names_out()
mean_scores = tfidf.mean(axis=0).A1
document_frequency = (tfidf > 0).sum(axis=0).A1
repeated_scores = [score for score, frequency in zip(mean_scores, document_frequency) if frequency >= 2]
threshold = sorted(repeated_scores)[max(0, len(repeated_scores) // 4 - 1)]
candidate_stopwords = {
    term for term, score, frequency in zip(terms, mean_scores, document_frequency)
    if frequency >= 2 and score <= threshold and term not in domain_terms
}


def preprocess(text, remove_stopwords=False, lemmatize=False):
    text = re.sub(r"https?://\S+|\S+@\S+", " ", text.lower())
    tokens = re.findall(r"[a-z]+", text)
    if remove_stopwords:
        tokens = [token for token in tokens if token not in candidate_stopwords]
    if lemmatize:
        tokens = [lemmatizer.lemmatize(token, pos="v") for token in tokens]
    return tokens

print("TF-IDF Candidate Stop-Words:")
print(", ".join(sorted(candidate_stopwords)) or "None")
print("\nTop TF-IDF Terms:")
for index in mean_scores.argsort()[::-1][:10]:
    print(f"{terms[index]:<18} {mean_scores[index]:.3f}")

configurations = [
    ("STOP ON + LEMMA ON", True, True),
    ("STOP ON + LEMMA OFF", True, False),
    ("STOP OFF + LEMMA ON", False, True),
    ("STOP OFF + LEMMA OFF", False, False),
]

print("\n" + "=" * 60)
print("PREPROCESSING RESULTS")
print("=" * 60)
for number, text in enumerate(texts, 1):
    print(f"\nTEXT {number}\nOriginal:\n{text}")
    for name, remove_stopwords, lemmatize in configurations:
        print(f"\n{name}:\n{' '.join(preprocess(text, remove_stopwords, lemmatize))}")

original_token_count = sum(len(text.split()) for text in clean_texts)
results = []
for name, remove_stopwords, lemmatize in configurations:
    all_tokens = []
    domain_count = 0
    information_scores = []
    for text in texts:
        tokens = preprocess(text, remove_stopwords, lemmatize)
        all_tokens.extend(tokens)
        domain_count += len(set(tokens) & domain_terms)
        information_scores.extend(mean_scores[list(terms).index(token)] for token in tokens if token in terms)
    token_count = len(all_tokens)
    noise_reduction = 1 - token_count / original_token_count
    domain_retention = domain_count / (len(domain_terms) * len(texts))
    information_retention = sum(information_scores) / len(information_scores) / max(mean_scores)
    score = 0.30 * noise_reduction + 0.40 * domain_retention + 0.30 * information_retention
    results.append((name, token_count, len(set(all_tokens)), domain_retention, information_retention, score))

print("\n" + "=" * 60)
print("CONFIGURATION COMPARISON")
print("=" * 60)
print(f"{'Configuration':<25} {'Tokens':>7} {'Vocab':>7} {'Domain%':>9} {'Info%':>8} {'Score':>8}")
print("-" * 70)
for result in results:
    print(f"{result[0]:<25} {result[1]:>7} {result[2]:>7} {result[3] * 100:>8.1f}% {result[4] * 100:>7.1f}% {result[5] * 100:>7.1f}")

best = max(results, key=lambda result: result[5])
print(f"\nBEST CONFIGURATION:\n{best[0]}")
print("\nFormula: Overall Score = 0.30 × Noise Reduction + 0.40 × Domain Term Retention + 0.30 × Information Retention")
print("The best configuration is selected automatically. The score balances noise reduction with SDLC-QA term and information retention.")

print("""
============================================================
SUMMARY
============================================================
Preprocessing cleans and normalizes text before NLP analysis.
Stopwords are low-information words that can add noise; candidates here are derived from repeated low TF-IDF terms.
TF-IDF measures word importance in a document relative to the document collection. With only three documents, this is a demonstration, not production-quality stop-word discovery.
Lemmatization maps related forms to a base word, such as testing → test, defects → defect, and releases → release.
The best configuration is task-dependent; this score balances noise reduction, domain-term retention, and information retention.

============================================================
AGENTIC AI CONNECTION
============================================================
An agent may receive messy requirements, Jira comments, test reports, emails, and release notes. This configurable preprocessing layer can clean and normalize them before retrieval, classification, summarization, or reasoning.
There is no universally correct configuration: an agent may choose different settings for search, classification, sentiment analysis, requirements analysis, or summarization.
""")
