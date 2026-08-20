from pathlib import Path

import nltk

nltk_data_dir = Path(__file__).parent / "nltk_data"
nltk_data_dir.mkdir(exist_ok=True)

if str(nltk_data_dir) not in nltk.data.path:
    nltk.data.path.insert(0, str(nltk_data_dir))

for resource, path in [("stopwords", "corpora/stopwords"), ("wordnet", "corpora/wordnet"), ("omw-1.4", "corpora/omw-1.4")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, download_dir=str(nltk_data_dir))

print(f"NLTK resources are ready in {nltk_data_dir}")
