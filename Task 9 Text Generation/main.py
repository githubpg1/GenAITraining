import re
import random
from pathlib import Path
from collections import Counter, defaultdict


# ============================================================
# PROBLEM 9 — TEXT GENERATION USING N-GRAMS
# ============================================================

print("=" * 70)
print("PROBLEM 9 — TEXT GENERATION USING N-GRAMS")
print("=" * 70)


# ============================================================
# 1. FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CORPUS_FILE = BASE_DIR / "data" / "sdlc_qa_corpus.txt"


# ============================================================
# 2. LOAD CORPUS
# ============================================================

print("\n" + "=" * 70)
print("LOADING CORPUS")
print("=" * 70)

if not CORPUS_FILE.exists():
    print(f"ERROR: Corpus file not found:")
    print(CORPUS_FILE)
    raise SystemExit(1)

text = CORPUS_FILE.read_text(encoding="utf-8")

words = text.split()

print(f"Corpus file : {CORPUS_FILE}")
print(f"Word count  : {len(words)}")

if len(words) < 5000:
    print("\nERROR: The corpus must contain at least 5,000 words.")
    print(f"Current word count: {len(words)}")
    raise SystemExit(1)

print("Corpus validation: PASSED")


# ============================================================
# 3. TOKENIZATION
# ============================================================

print("\n" + "=" * 70)
print("TOKENIZATION")
print("=" * 70)


def tokenize(text):
    """
    Convert text into lowercase word tokens.

    Punctuation is removed so that the N-gram models
    learn primarily from word sequences.
    """

    text = text.lower()

    tokens = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", text)

    return tokens


tokens = tokenize(text)

print(f"Tokens generated: {len(tokens)}")

print("\nFirst 30 tokens:")
print(tokens[:30])


# ============================================================
# 4. CREATE N-GRAM MODEL
# ============================================================

print("\n" + "=" * 70)
print("BUILDING N-GRAM MODELS")
print("=" * 70)


def build_ngram_model(tokens, n):
    """
    Build an N-gram language model.

    Example for a trigram:

        "qa team completed testing"

    becomes:

        ("qa", "team") -> "completed"
        ("team", "completed") -> "testing"

    The model stores possible next words for every context.
    """

    model = defaultdict(list)

    for i in range(len(tokens) - n + 1):

        context = tuple(tokens[i:i + n - 1])
        next_word = tokens[i + n - 1]

        model[context].append(next_word)

    return model


bigram_model = build_ngram_model(tokens, 2)
trigram_model = build_ngram_model(tokens, 3)
fourgram_model = build_ngram_model(tokens, 4)


print(f"Bigram contexts  : {len(bigram_model)}")
print(f"Trigram contexts : {len(trigram_model)}")
print(f"Four-gram contexts: {len(fourgram_model)}")


# ============================================================
# 5. GENERATE TEXT
# ============================================================

print("\n" + "=" * 70)
print("TEXT GENERATION")
print("=" * 70)


SEED = "the qa team"

TARGET_WORDS = 50


def generate_text(model, n, seed, target_words=50, random_seed=42):
    """
    Generate text using an N-gram model.

    The same random seed is used for reproducibility.
    """

    random.seed(random_seed)

    seed_tokens = tokenize(seed)

    # The model requires n-1 words as the initial context.
    required_context_size = n - 1

    if len(seed_tokens) < required_context_size:
        raise ValueError(
            f"Seed must contain at least {required_context_size} words "
            f"for an {n}-gram model."
        )

    # Use the last n-1 seed words as context.
    generated = seed_tokens.copy()

    context = tuple(generated[-required_context_size:])

    while len(generated) < target_words:

        # If the current context exists, choose one of its
        # possible next words.
        if context in model:

            possible_words = model[context]

            next_word = random.choice(possible_words)

        else:
            # Context not found.
            # Fall back to a random context from the model.
            context = random.choice(list(model.keys()))

            possible_words = model[context]

            next_word = random.choice(possible_words)

        generated.append(next_word)

        context = tuple(generated[-required_context_size:])

    return generated[:target_words]


# ============================================================
# 6. GENERATE BIGRAM PASSAGE
# ============================================================

bigram_output = generate_text(
    bigram_model,
    n=2,
    seed=SEED,
    target_words=TARGET_WORDS,
    random_seed=42
)


# ============================================================
# 7. GENERATE TRIGRAM PASSAGE
# ============================================================

trigram_output = generate_text(
    trigram_model,
    n=3,
    seed=SEED,
    target_words=TARGET_WORDS,
    random_seed=42
)


# ============================================================
# 8. GENERATE FOUR-GRAM PASSAGE
# ============================================================

fourgram_output = generate_text(
    fourgram_model,
    n=4,
    seed=SEED,
    target_words=TARGET_WORDS,
    random_seed=42
)


# ============================================================
# 9. DISPLAY GENERATED TEXT
# ============================================================


def display_passage(title, generated_words):
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)

    print(" ".join(generated_words))

    print(f"\nGenerated words: {len(generated_words)}")


display_passage(
    "BIGRAM — 2-GRAM MODEL",
    bigram_output
)

display_passage(
    "TRIGRAM — 3-GRAM MODEL",
    trigram_output
)

display_passage(
    "FOUR-GRAM — 4-GRAM MODEL",
    fourgram_output
)


# ============================================================
# 10. N-GRAM STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("MODEL STATISTICS")
print("=" * 70)


def calculate_unique_ratio(generated_words):
    """
    Percentage of generated words that are unique.
    """

    if not generated_words:
        return 0

    return len(set(generated_words)) / len(generated_words)


def calculate_source_overlap(generated_words, source_tokens):
    """
    Calculate the percentage of generated words that also
    appear somewhere in the source corpus.

    Since the model learned directly from this corpus,
    high overlap is expected.
    """

    source_vocabulary = set(source_tokens)

    matching_words = sum(
        1 for word in generated_words
        if word in source_vocabulary
    )

    return matching_words / len(generated_words)


def calculate_repeated_ngram_ratio(generated_words, n):
    """
    Measures how much of the generated text consists of
    repeated N-grams.

    Higher values indicate more repetition.
    """

    if len(generated_words) < n:
        return 0

    ngrams = [
        tuple(generated_words[i:i + n])
        for i in range(len(generated_words) - n + 1)
    ]

    counts = Counter(ngrams)

    repeated = sum(
        count
        for count in counts.values()
        if count > 1
    )

    return repeated / len(ngrams)


models = [
    ("Bigram", bigram_output, 2),
    ("Trigram", trigram_output, 3),
    ("Four-gram", fourgram_output, 4),
]


for name, output, n in models:

    unique_ratio = calculate_unique_ratio(output)

    source_overlap = calculate_source_overlap(
        output,
        tokens
    )

    repetition = calculate_repeated_ngram_ratio(
        output,
        n
    )

    print(f"\n{name}")

    print(
        f"Unique word ratio       : "
        f"{unique_ratio:.2f}"
    )

    print(
        f"Source vocabulary overlap: "
        f"{source_overlap:.2f}"
    )

    print(
        f"Repeated {n}-gram ratio  : "
        f"{repetition:.2f}"
    )


# ============================================================
# 11. SOURCE COPYING ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SOURCE COPYING ANALYSIS")
print("=" * 70)


def longest_matching_sequence(generated, source):
    """
    Find the longest consecutive sequence of generated words
    that appears somewhere in the source corpus.

    This provides a simple indication of source copying.
    """

    source_positions = defaultdict(list)

    for index, word in enumerate(source):
        source_positions[word].append(index)

    longest = 0

    for generated_index, word in enumerate(generated):

        if word not in source_positions:
            continue

        for source_index in source_positions[word]:

            length = 0

            while (
                generated_index + length < len(generated)
                and source_index + length < len(source)
                and generated[generated_index + length]
                == source[source_index + length]
            ):
                length += 1

            longest = max(longest, length)

    return longest


for name, output, _ in models:

    longest_match = longest_matching_sequence(
        output,
        tokens
    )

    print(
        f"{name:10s} longest source sequence copied: "
        f"{longest_match} words"
    )


# ============================================================
# 12. SIMPLE MODEL INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("MODEL INTERPRETATION")
print("=" * 70)

print("""
BIGRAM
------
Uses only one previous word to predict the next word.

Advantages:
- Produces more variety.
- Can generate different combinations.
- Less likely to copy long phrases exactly.

Disadvantages:
- Often loses sentence-level context.
- Can sound less coherent.
""")


print("""
TRIGRAM
-------
Uses two previous words to predict the next word.

Advantages:
- Better local context than a bigram.
- Usually produces more fluent phrases.
- Maintains common word combinations better.

Disadvantages:
- Has less flexibility than a bigram.
- Can still produce repetitive patterns.
""")


print("""
FOUR-GRAM
---------
Uses three previous words to predict the next word.

Advantages:
- Maintains more local context.
- Can produce highly fluent phrases when the context
  exists in the training corpus.

Disadvantages:
- More likely to reproduce phrases from the source.
- Has fewer possible contexts.
- Can fall back to another context when an unseen
  context is encountered.
""")


# ============================================================
# 13. DETERMINE WHICH MODEL IS MOST FLUENT
# ============================================================

print("\n" + "=" * 70)
print("FLUENCY AND COPYING CONCLUSION")
print("=" * 70)


print("""
For a small domain corpus, the expected behavior is:

Bigram
  → More varied but less coherent.

Trigram
  → Usually a good balance between coherence and variety.

Four-gram
  → Usually the most locally fluent because it uses more
    context, but it is also more likely to reproduce
    phrases that appeared in the training corpus.

Therefore:

Most fluent:
  Usually the FOUR-GRAM model.

Most likely to copy the source:
  Usually the FOUR-GRAM model.

Best balance:
  Usually the TRIGRAM model.

However, the actual generated passages and copying statistics
should be examined rather than assuming the result.
""")


# ============================================================
# 14. FINAL ANSWER TO THE ASSIGNMENT
# ============================================================

print("\n" + "=" * 70)
print("ANSWER TO PROBLEM 9")
print("=" * 70)

print("""
Question:
Which model is most fluent, and which one just copies the source?

Answer:

The bigram model has the least context because it considers only
one previous word. It therefore tends to produce more varied but
less coherent text.

The trigram model considers two previous words and generally gives
a better balance between fluency and variation.

The four-gram model considers three previous words and can produce
the most fluent local phrases because it has more context. However,
because N-gram models learn exact word sequences from the training
corpus, the four-gram model can also reproduce longer phrases from
the original source.

This demonstrates an important limitation of traditional N-gram
language models:

More context can improve local fluency, but it can also increase
the likelihood of memorizing and copying training text.
""")


# ============================================================
# 15. AGENTIC AI CONNECTION
# ============================================================

print("\n" + "=" * 70)
print("AGENTIC AI CONNECTION")
print("=" * 70)

print("""
An N-gram model is not itself an Agentic AI system.

It is a simple statistical language model that can generate text
based on patterns learned from a domain corpus.

In an SDLC Governance Agent, similar language-generation concepts
could be used for:

- Generating draft governance summaries
- Completing short pieces of domain text
- Producing draft status statements
- Generating example test descriptions
- Supporting automated documentation

However, modern governance agents would normally use much more
advanced language models rather than simple N-grams.

The N-gram exercise is useful because it demonstrates a fundamental
NLP concept:

Training corpus
      ↓
Learn word-sequence probabilities
      ↓
Provide a seed
      ↓
Predict the next word
      ↓
Generate a passage
""")


# ============================================================
# 16. LIMITATIONS
# ============================================================

print("\n" + "=" * 70)
print("LIMITATIONS")
print("=" * 70)

print("""
1. N-gram models only consider a limited amount of previous context.

2. Higher-order N-grams require many examples of specific word
   sequences.

3. A small corpus can cause sparse or unseen contexts.

4. Higher-order models may copy phrases directly from the training
   corpus.

5. N-grams do not understand the meaning of the text.

6. They do not understand long-range relationships between words.

7. The generated text can become repetitive or grammatically awkward.

8. Modern Transformer-based language models are significantly more
   capable of understanding context and generating coherent text.

9. The fluency comparison in this classroom exercise is qualitative
   and supported by simple statistics rather than a sophisticated
   language-quality metric.
""")


print("\n" + "=" * 70)
print("PROBLEM 9 COMPLETE")
print("=" * 70)