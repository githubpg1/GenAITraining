import re
from pathlib import Path

from gensim.models import Word2Vec

sentences_file = Path(__file__).parent / "data" / "sdlc_qa_sentences.txt"
text = sentences_file.read_text(encoding="utf-8").splitlines()
sentences = [re.findall(r"[a-z]+", sentence.lower()) for sentence in text if sentence.strip()]

model = Word2Vec(
    sentences=sentences,
    vector_size=50,
    window=3,
    min_count=1,
    workers=1,
    seed=42,
)

print("Word2Vec — SDLC-QA Domain")
print("==========================")
print(f"\nTraining sentences: {len(sentences)}")
print("\nMost similar words:")

for word in ["requirement", "testing", "defect", "test", "release"]:
    print(f"\n{word}")
    for similar_word, score in model.wv.most_similar(word, topn=3):
        print(f"  {similar_word:<15} {score:.3f}")

print("""

What the results mean:
Word2Vec does not learn dictionary definitions or synonyms. It learns relationships
from the contexts in which words appear. For example, defect may be related to
issue, failure, or retesting because those terms occur in similar QA contexts.
The requirement, acceptance criteria, and testing relationship reflects an SDLC-QA
pattern learned from the training sentences.

Agentic AI connection:
Word2Vec can provide domain-specific word representations that help an AI system
discover related SDLC-QA terminology. In an agentic workflow, these relationships
can support related-term discovery, search, retrieval, issue grouping, and context
expansion.
Word2Vec itself is not an AI agent. It is a word-representation technique that can
be used as one component of a larger AI or agentic system.

Limitation:
This model is trained on only 25 sentences for demonstration purposes. Therefore,
the similarity results depend heavily on the supplied SDLC-QA sentences and should
not be considered production-quality semantic relationships.
""")
