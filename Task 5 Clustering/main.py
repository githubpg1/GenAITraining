"""End-to-end financial NLP analysis using Word2Vec and clustering."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "financial_sentences.txt"
PLOT_FILE = PROJECT_DIR / "financial_clusters_pca.png"
KEY_WORDS = ["credit", "loan", "transaction", "risk", "investment"]
STOP_WORDS = {"a", "an", "and", "are", "as", "at", "be", "before", "but", "by", "can", "for", "from", "has", "have", "helps", "in", "is", "may", "of", "on", "or", "the", "their", "these", "to", "using", "was", "with"}


def tokenize(sentence: str) -> List[str]:
    """Lowercase, remove punctuation, and retain meaningful words."""
    words = re.findall(r"[a-z]+(?:-[a-z]+)?", sentence.lower())
    normalized = []
    # Normalize plural forms so the requested key words are present even when
    # the source sentence uses a plural, such as ``transactions``.
    singular_forms = {
        "transactions": "transaction",
        "investments": "investment",
        "portfolios": "portfolio",
        "payments": "payment",
        "loans": "loan",
        "risks": "risk",
    }
    for word in words:
        if word in STOP_WORDS:
            continue
        word = singular_forms.get(word, word)
        normalized.append(word.replace("-", "_"))
    return normalized


def load_sentences() -> List[str]:
    sentences = [line.strip() for line in DATA_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(sentences) != 25:
        raise ValueError(f"Expected exactly 25 sentences, found {len(sentences)}")
    return sentences


def sentence_embeddings(model: Word2Vec, tokenized: List[List[str]]) -> np.ndarray:
    vectors = []
    for tokens in tokenized:
        known = [model.wv[word] for word in tokens if word in model.wv]
        vectors.append(np.mean(known, axis=0) if known else np.zeros(model.vector_size))
    return np.asarray(vectors)


def interpretation(cluster: int, frame: pd.DataFrame, tokenized: List[List[str]]) -> None:
    rows = frame[frame["Cluster"] == cluster]
    counts: Dict[str, int] = {}
    for sentence_number in rows["Sentence Number"]:
        for word in tokenized[int(sentence_number) - 1]:
            counts[word] = counts.get(word, 0) + 1
    concepts = ", ".join(word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:6])
    print(f"\nCluster {cluster}\n{'-' * 40}")
    print(f"Theme: {concepts or 'No known terms'}")
    print(f"Number of sentences: {len(rows)}")
    print(f"Key financial concepts: {concepts or 'None'}")
    print("Explanation: This theme is based on the most frequent preprocessed terms in the assigned sentences.")
    print("Representative sentences:")
    for _, row in rows.head(3).iterrows():
        print(f"  {int(row['Sentence Number'])}. {row['Text']}")


def main() -> None:
    print("=" * 60)
    print("FINANCIAL NLP ANALYSIS")
    print("=" * 60)
    sentences = load_sentences()
    print("\n1. DATASET\n" + "-" * 60)
    print(f"Number of sentences: {len(sentences)}")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")

    tokenized = [tokenize(sentence) for sentence in sentences]
    print("\n2. TEXT PREPROCESSING\n" + "-" * 60)
    for i in [0, 4, 23]:
        print(f"Original: {sentences[i]}")
        print(f"Processed: {tokenized[i]}")

    parameters = dict(vector_size=100, window=5, min_count=1, workers=4, sg=1, epochs=100, seed=42)
    model = Word2Vec(sentences=tokenized, **parameters)
    print("\n3. WORD2VEC MODEL\n" + "-" * 60)
    print(f"Training sentences: {len(tokenized)}")
    print(f"Vocabulary size: {len(model.wv)}")
    print(f"Vector dimensions: {model.vector_size}")
    print(f"Training parameters: {parameters}")

    print("\n4. SEMANTIC SIMILARITY\n" + "-" * 60)
    similarity_results = {}
    for word in KEY_WORDS:
        if word not in model.wv:
            raise ValueError(f"Missing key word: {word}")
        similarity_results[word] = model.wv.most_similar(word, topn=3)
        print(f"\nKey Word: {word}")
        for rank, (similar, score) in enumerate(similarity_results[word], 1):
            print(f"{rank}. {similar} — similarity: {score:.4f}")

    print("\n5. WORD2VEC PATTERN ANALYSIS\n" + "-" * 60)
    print("Actual model patterns:")
    for word, results in similarity_results.items():
        print(f"- {word}: {', '.join(similar for similar, _ in results)}")
    print("These relationships are interpreted from the actual similarity output, not predetermined labels.")
    print("Limitation: The Word2Vec model is trained on only 25 sentences, so the learned semantic relationships are educational and illustrative rather than production-quality financial language representations.")

    embeddings = sentence_embeddings(model, tokenized)
    if embeddings.shape != (25, 100):
        raise ValueError(f"Unexpected embedding shape: {embeddings.shape}")
    print("\n6. SENTENCE EMBEDDINGS\n" + "-" * 60)
    print(f"Embedding shape: {embeddings.shape}")

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)
    if len(labels) != 25 or len(set(labels)) != 4:
        raise ValueError("KMeans validation failed")
    assignments = pd.DataFrame({"Sentence Number": range(1, 26), "Cluster": labels, "Text": sentences}).sort_values(["Cluster", "Sentence Number"])
    print("\n7. KMEANS CLUSTERING\n" + "-" * 60)
    print("Number of clusters: 4")
    print(assignments.to_string(index=False))

    print("\n8. CLUSTER INTERPRETATION\n" + "-" * 60)
    for cluster in range(4):
        interpretation(cluster, assignments, tokenized)

    pca = PCA(n_components=2, random_state=42)
    coordinates = pca.fit_transform(embeddings)
    if coordinates.shape != (25, 2):
        raise ValueError(f"Unexpected PCA shape: {coordinates.shape}")
    print("\n9. PCA ANALYSIS\n" + "-" * 60)
    print(f"PCA Component 1 explained variance: {pca.explained_variance_ratio_[0]:.4f}")
    print(f"PCA Component 2 explained variance: {pca.explained_variance_ratio_[1]:.4f}")
    print(f"Total explained variance: {pca.explained_variance_ratio_.sum():.4f}")

    # Use short word-based labels on the plot instead of sentence numbers.
    # The first three processed words provide readable, domain-relevant labels.
    word_labels = [" ".join(words[:3]) for words in tokenized]
    plot_frame = pd.DataFrame({"Component 1": coordinates[:, 0], "Component 2": coordinates[:, 1], "Cluster": labels, "Label": word_labels})
    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(14, 10))
    ax = sns.scatterplot(data=plot_frame, x="Component 1", y="Component 2", hue="Cluster", palette="deep", s=130, style="Cluster")
    for _, row in plot_frame.iterrows():
        ax.annotate(row["Label"], (row["Component 1"], row["Component 2"]), xytext=(5, 5), textcoords="offset points", fontsize=8)
    ax.set_title("Financial Sentence Clustering using Word2Vec + KMeans + PCA")
    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=180)
    plt.close()
    if not PLOT_FILE.exists():
        raise FileNotFoundError(PLOT_FILE)
    print("\n10. VISUALIZATION\n" + "-" * 60)
    print(PLOT_FILE)
    print("\n" + "=" * 60 + "\nANALYSIS COMPLETE\n" + "=" * 60)


if __name__ == "__main__":
    main()
