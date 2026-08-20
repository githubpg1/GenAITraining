from pathlib import Path

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
words_file = Path(__file__).parent / "data" / "words.txt"
words = [word.strip() for word in words_file.read_text(encoding="utf-8").splitlines() if word.strip()]

print(f"{'Original':<12} | {'Stemmed':<12} | {'Lemmatized':<12}")
print("-" * 51)

for word in words:
    print(f"{word:<12} | {stemmer.stem(word):<12} | {lemmatizer.lemmatize(word, pos='v'):<12}")

print("\nFor NLP text processing, lemmatization is generally better because it produces meaningful dictionary words using linguistic knowledge.")
