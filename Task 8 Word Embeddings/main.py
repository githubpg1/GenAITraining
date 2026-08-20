import os
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# ============================================================
# PROBLEM 8 — WORD EMBEDDINGS & SEMANTIC CLUSTERING
# SDLC-QA DOMAIN
# ============================================================

print("=" * 70)
print("PROBLEM 8 — WORD EMBEDDINGS & SEMANTIC CLUSTERING")
print("=" * 70)


# ============================================================
# 1. FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "sdlc_qa_records.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "sdlc_qa_clusters.png"
)


# ============================================================
# 2. PROBLEM 7 PREPROCESSING CONFIGURATION
# ============================================================
#
# Problem 7 tested four preprocessing configurations:
#
# 1. Stopwords OFF + Lemmatization OFF
# 2. Stopwords OFF + Lemmatization ON
# 3. Stopwords ON  + Lemmatization OFF  <-- BEST
# 4. Stopwords ON  + Lemmatization ON
#
# Based on Problem 7 results, Task 8 directly uses:
#
#     Stopwords = ON
#     Lemmatization = OFF
#
# We do NOT test the four configurations again.
# ============================================================

REMOVE_STOPWORDS = True
LEMMATIZE = False


# ============================================================
# 3. STOPWORDS
# ============================================================
#
# IMPORTANT:
# Ideally, this set should be the TF-IDF-derived stopword set
# produced in Problem 7.
#
# If your Problem 7 implementation already has a stopword
# function, replace this set with that function/result.
#
# The words below are common low-information words for this
# demonstration dataset.
# ============================================================

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "is",
    "are",
    "was",
    "were",
    "to",
    "of",
    "for",
    "in",
    "on",
    "with",
    "after",
    "before",
    "that",
    "this",
    "from",
    "by",
    "as",
    "at",
    "be",
    "has",
    "have",
    "had",
    "it",
    "its",
    "their",
    "they",
    "them",
    "than",
    "into",
    "during",
    "through",
    "about",
    "over",
    "under",
    "between",
    "then",
    "when",
    "while",
    "also",
}


# ============================================================
# 4. PREPROCESS FUNCTION
# ============================================================

def preprocess(
    text,
    remove_stopwords=True,
    lemmatize=False
):
    """
    Clean one SDLC-QA record.

    Problem 7 best configuration:
        remove_stopwords=True
        lemmatize=False

    Steps:
        1. Lowercase
        2. Remove URLs
        3. Remove email addresses
        4. Remove punctuation
        5. Normalize whitespace
        6. Tokenize
        7. Remove stopwords
        8. No lemmatization
    """

    # --------------------------------------------------------
    # 1. Convert to string and lowercase
    # --------------------------------------------------------

    text = str(text).lower()

    # --------------------------------------------------------
    # 2. Remove URLs
    # --------------------------------------------------------

    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # --------------------------------------------------------
    # 3. Remove email addresses
    # --------------------------------------------------------

    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # --------------------------------------------------------
    # 4. Remove punctuation
    # --------------------------------------------------------

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    # --------------------------------------------------------
    # 5. Normalize whitespace
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # --------------------------------------------------------
    # 6. Tokenization
    # --------------------------------------------------------

    tokens = text.split()

    # --------------------------------------------------------
    # 7. Stopword removal
    # --------------------------------------------------------

    if remove_stopwords:

        tokens = [
            word
            for word in tokens
            if word not in STOPWORDS
        ]

    # --------------------------------------------------------
    # 8. Lemmatization
    # --------------------------------------------------------
    #
    # Problem 7 showed that lemmatization OFF performed best.
    #
    # Therefore, no lemmatization is performed here.
    # --------------------------------------------------------

    if lemmatize:
        raise ValueError(
            "Task 8 is configured to use the Problem 7 best "
            "configuration: lemmatization=False."
        )

    return tokens


# ============================================================
# 5. LOAD DATA WITH PANDAS
# ============================================================

if not os.path.exists(DATA_FILE):

    print("\nERROR: Dataset not found:")
    print(DATA_FILE)

    raise SystemExit(1)


df = pd.read_csv(DATA_FILE)

print(f"\nRecords loaded: {len(df)}")


# Validate record count

if len(df) < 200:

    print(
        "ERROR: Dataset must contain at least 200 records."
    )

    raise SystemExit(1)


# Validate text column

if "text" not in df.columns:

    print(
        "ERROR: CSV must contain a 'text' column."
    )

    raise SystemExit(1)


# ============================================================
# 6. PREPROCESSING
# ============================================================

print("\n")
print("=" * 70)
print("PREPROCESSING")
print("=" * 70)

print(
    "\nUsing the best preprocessing configuration from Problem 7:"
)

print("Stopword removal : ON")
print("Lemmatization    : OFF")


# Apply preprocessing

df["tokens"] = df["text"].apply(
    lambda text: preprocess(
        text,
        remove_stopwords=REMOVE_STOPWORDS,
        lemmatize=LEMMATIZE
    )
)


tokenized_records = df["tokens"].tolist()


# ------------------------------------------------------------
# Display a few examples
# ------------------------------------------------------------

print("\nExample cleaned records:")

for i in range(min(5, len(df))):

    print(
        f"\nOriginal : {df.loc[i, 'text']}"
    )

    print(
        f"Cleaned  : {' '.join(df.loc[i, 'tokens'])}"
    )


# ============================================================
# 7. TRAIN WORD2VEC
# ============================================================

print("\n")
print("=" * 70)
print("WORD2VEC")
print("=" * 70)

print("\nTraining Word2Vec...")


model = Word2Vec(
    sentences=tokenized_records,
    vector_size=50,
    window=5,
    min_count=1,
    workers=1,
    seed=42,
    epochs=100
)


print(
    f"Word2Vec vocabulary size: {len(model.wv)}"
)


# ============================================================
# 8. DOCUMENT / RECORD VECTOR
# ============================================================

def document_vector(tokens, model):
    """
    Create one vector representing a complete record.

    The record vector is the average of the Word2Vec
    vectors of all in-vocabulary words.
    """

    vectors = []

    for token in tokens:

        if token in model.wv:

            vectors.append(
                model.wv[token]
            )

    # No known words

    if not vectors:

        return [0.0] * model.vector_size

    # Average word vectors

    return sum(vectors) / len(vectors)


# ============================================================
# 9. CREATE RECORD VECTORS
# ============================================================

print("\nCreating document vectors...")


record_vectors = []

for tokens in tokenized_records:

    vector = document_vector(
        tokens,
        model
    )

    record_vectors.append(vector)


# Convert to DataFrame/NumPy-compatible matrix

record_vectors = pd.DataFrame(
    record_vectors
).values


# Count zero vectors

zero_vector_count = sum(
    1
    for vector in record_vectors
    if not vector.any()
)


print(
    "Records with no in-vocabulary words: "
    f"{zero_vector_count}"
)


print(
    f"Record vector dimensions: "
    f"{record_vectors.shape[1]}"
)


# ============================================================
# 10. KMEANS
# ============================================================

print("\n")
print("=" * 70)
print("KMEANS CLUSTERING")
print("=" * 70)


print("\nRunning KMeans...")


n_clusters = 5


kmeans = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init=10
)


# IMPORTANT:
# KMeans runs on the ORIGINAL 50-dimensional vectors.
#
# PCA is NOT used for clustering.

cluster_labels = kmeans.fit_predict(
    record_vectors
)


df["cluster"] = cluster_labels


# ============================================================
# 11. CLUSTER DISTRIBUTION
# ============================================================

print("\nCluster distribution:")


cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
)


for cluster_id, count in cluster_counts.items():

    print(
        f"Cluster {cluster_id}: "
        f"{count} records"
    )


# ============================================================
# 12. DOMAIN TOPICS
# ============================================================
#
# These vocabularies are NOT used to perform clustering.
#
# They are only used AFTER KMeans to help interpret the
# discovered clusters.
# ============================================================

cluster_topics = {

    "Requirements": [
        "requirement",
        "story",
        "acceptance",
        "criteria",
        "business",
        "user"
    ],

    "Testing / QA": [
        "test",
        "testing",
        "regression",
        "coverage",
        "automation",
        "validation",
        "integration",
        "qa"
    ],

    "Defects": [
        "defect",
        "bug",
        "failure",
        "fix",
        "retest",
        "severity",
        "priority",
        "issue"
    ],

    "Release": [
        "release",
        "deployment",
        "production",
        "readiness",
        "approval",
        "blocker",
        "rollback"
    ],

    "Governance": [
        "traceability",
        "scope",
        "approval",
        "governance",
        "status",
        "risk",
        "steering",
        "board",
        "evidence"
    ]
}


# ============================================================
# 13. INTERPRET CLUSTERS
# ============================================================

cluster_interpretations = {}


print("\n")
print("=" * 70)
print("CLUSTER INTERPRETATION")
print("=" * 70)


for cluster_id in range(n_clusters):

    cluster_df = df[
        df["cluster"] == cluster_id
    ]


    # --------------------------------------------------------
    # Collect tokens
    # --------------------------------------------------------

    cluster_tokens = []

    for tokens in cluster_df["tokens"]:

        cluster_tokens.extend(tokens)


    # --------------------------------------------------------
    # Count terms
    # --------------------------------------------------------

    word_counts = Counter(
        cluster_tokens
    )


    # Top 10 terms

    top_terms = [
        word
        for word, count
        in word_counts.most_common(10)
    ]


    # --------------------------------------------------------
    # Score domain topics
    # --------------------------------------------------------

    topic_scores = {}


    for topic, topic_words in cluster_topics.items():

        score = 0

        for word in topic_words:

            score += word_counts.get(
                word,
                0
            )

        topic_scores[topic] = score


    # --------------------------------------------------------
    # Find best topic
    # --------------------------------------------------------

    likely_topic = max(
        topic_scores,
        key=topic_scores.get
    )


    # If no topic words match

    if topic_scores[likely_topic] == 0:

        likely_topic = "Mixed / Other"


    # Store interpretation

    cluster_interpretations[
        cluster_id
    ] = {

        "topic": likely_topic,

        "terms": top_terms,

        "scores": topic_scores
    }


    # --------------------------------------------------------
    # Print cluster information
    # --------------------------------------------------------

    print("\n" + "=" * 60)

    print(
        f"CLUSTER {cluster_id}"
    )

    print("=" * 60)


    print(
        f"Records: {len(cluster_df)}"
    )


    print(
        "\nTop terms:"
    )

    print(
        ", ".join(top_terms)
    )


    print(
        "\nTopic scores:"
    )


    sorted_scores = sorted(
        topic_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )


    for topic, score in sorted_scores:

        print(
            f"  {topic}: {score}"
        )


    print(
        f"\nLikely interpretation: "
        f"{likely_topic}"
    )


    # --------------------------------------------------------
    # Representative records
    # --------------------------------------------------------

    cluster_indices = (
        cluster_df.index.tolist()
    )


    centroid = (
        kmeans.cluster_centers_[cluster_id]
    )


    distances = []


    for index in cluster_indices:

        vector = record_vectors[index]


        distance = (
            (vector - centroid) ** 2
        ).sum()


        distances.append(
            (index, distance)
        )


    # Closest to centroid

    distances.sort(
        key=lambda item: item[1]
    )


    print(
        "\nRepresentative records:"
    )


    for index, distance in distances[:3]:

        print(
            f"- {df.loc[index, 'text']}"
        )


# ============================================================
# 14. CREATE CLUSTER NAMES
# ============================================================

cluster_names = {}


for cluster_id in range(n_clusters):

    cluster_names[
        cluster_id
    ] = cluster_interpretations[
        cluster_id
    ]["topic"]


# ============================================================
# 15. PCA
# ============================================================

print("\n")
print("=" * 70)
print("PCA VISUALIZATION")
print("=" * 70)


print(
    "\nPCA reduces the 50-dimensional Word2Vec "
    "record vectors to two dimensions."
)


print(
    "PCA is used only for visualization."
)


print(
    "KMeans was performed on the original "
    "Word2Vec record vectors."
)


pca = PCA(
    n_components=2
)


vectors_2d = pca.fit_transform(
    record_vectors
)


print(
    "\nPCA explained variance:"
)


print(
    f"Component 1: "
    f"{pca.explained_variance_ratio_[0]:.4f}"
)


print(
    f"Component 2: "
    f"{pca.explained_variance_ratio_[1]:.4f}"
)


print(
    f"Total: "
    f"{pca.explained_variance_ratio_.sum():.4f}"
)


# ============================================================
# 16. CREATE PCA PLOT
# ============================================================

plt.figure(
    figsize=(14, 9)
)


colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd"
]


# ------------------------------------------------------------
# Plot each cluster
# ------------------------------------------------------------

for cluster_id in range(n_clusters):

    mask = (
        df["cluster"] == cluster_id
    )


    plt.scatter(
        vectors_2d[mask, 0],
        vectors_2d[mask, 1],
        s=65,
        alpha=0.75,
        color=colors[cluster_id],
        label=(
            f"Cluster {cluster_id}: "
            f"{cluster_names[cluster_id]}"
        )
    )


# ============================================================
# 17. WRITE CLUSTER NAMES DIRECTLY ON THE PLOT
# ============================================================

for cluster_id in range(n_clusters):

    mask = (
        df["cluster"] == cluster_id
    )


    # PCA center of cluster

    center_x = (
        vectors_2d[mask, 0].mean()
    )

    center_y = (
        vectors_2d[mask, 1].mean()
    )


    cluster_name = (
        cluster_names[cluster_id]
    )


    # --------------------------------------------------------
    # Write topic name at cluster center
    # --------------------------------------------------------

    plt.annotate(

        cluster_name,

        xy=(
            center_x,
            center_y
        ),

        xytext=(
            0,
            15
        ),

        textcoords="offset points",

        ha="center",

        fontsize=12,

        fontweight="bold",

        bbox=dict(

            boxstyle="round,pad=0.5",

            facecolor="white",

            edgecolor=colors[
                cluster_id
            ],

            linewidth=2,

            alpha=0.95
        )
    )


# ============================================================
# 18. PLOT FORMATTING
# ============================================================

plt.title(
    "SDLC-QA Semantic Clusters\n"
    "Word2Vec + KMeans + PCA",
    fontsize=16,
    fontweight="bold"
)


plt.xlabel(
    "PCA Component 1",
    fontsize=12
)


plt.ylabel(
    "PCA Component 2",
    fontsize=12
)


plt.legend(
    title="Discovered Clusters",
    bbox_to_anchor=(
        1.02,
        1
    ),
    loc="upper left"
)


plt.grid(
    True,
    linestyle="--",
    alpha=0.3
)


plt.tight_layout()


# ============================================================
# 19. SAVE PLOT
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)


print(
    "\nPCA plot saved to:"
)


print(
    OUTPUT_FILE
)


# Display plot

plt.show()


# ============================================================
# 20. FINAL CLUSTER SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("CLUSTER SUMMARY")
print("=" * 70)


for cluster_id in range(n_clusters):

    topic = cluster_names[
        cluster_id
    ]


    terms = cluster_interpretations[
        cluster_id
    ]["terms"]


    print(
        f"\nCluster {cluster_id} → {topic}"
    )


    print(
        "Reason: Dominant terms include "
        + ", ".join(terms[:6])
        + "."
    )


# ============================================================
# 21. AGENTIC AI CONNECTION
# ============================================================

print("\n")
print("=" * 70)
print("AGENTIC AI CONNECTION")
print("=" * 70)


print("""
Jira / Requirements / Test / Defect / Release records
                        ↓
             Problem 7 Preprocessing
                        ↓
          Stopwords ON / Lemmatization OFF
                        ↓
                    Word2Vec
                        ↓
             Average Word Vectors
                        ↓
                 Record Vectors
                        ↓
                    KMeans
                        ↓
              Semantic Clusters
                        ↓
             Governance / QA Agent

This approach could help an SDLC Governance Agent:

- Group related requirements
- Group similar defects
- Identify testing themes
- Discover release-readiness issues
- Organize large volumes of SDLC records
- Identify emerging delivery-risk themes
- Support retrieval and governance reporting

Word2Vec + KMeans is not itself an Agentic AI system.
It is an NLP/ML component that could provide semantic
organization capabilities to a larger agentic workflow.
""")


# ============================================================
# 22. LIMITATIONS
# ============================================================

print("=" * 70)
print("LIMITATIONS")
print("=" * 70)


print("""
1. 200–250 records are sufficient for a classroom demonstration
   but small for production-quality Word2Vec.

2. Averaging word vectors loses word order and some contextual
   information.

3. KMeans requires choosing the number of clusters.

4. Cluster labels are not automatically meaningful and require
   interpretation.

5. PCA is mainly a visualization technique and may not preserve
   every semantic relationship.

6. Modern Transformer embeddings are generally more powerful
   than Word2Vec for semantic similarity, but Word2Vec is useful
   for understanding the fundamental concept.
""")


# ============================================================
# 23. FINAL SUMMARY
# ============================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)


print("""
Word2Vec:
Learns numerical representations of words based on their context.

Record embedding:
Averages the Word2Vec vectors of the words in each record to create
one numerical vector representing the complete record.

KMeans:
Groups records whose Word2Vec record vectors are relatively similar.

PCA:
Reduces the high-dimensional vectors to two dimensions so that
the semantic clusters can be visualized.

Semantic clustering:
Groups records based on learned language/context relationships
rather than exact keyword matching.

Problem 7 preprocessing:
The best-performing configuration was selected before Word2Vec:

    Stopwords     = ON
    Lemmatization = OFF

Therefore, Task 8 uses this configuration directly and does not
repeat the four preprocessing experiments.
""")


print("=" * 70)
print("PROBLEM 8 COMPLETE")
print("=" * 70)