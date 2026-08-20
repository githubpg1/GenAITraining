# Financial TF-IDF Analysis

This beginner-friendly application analyzes exactly eight financial-domain documents with `sklearn.feature_extraction.text.TfidfVectorizer`.

## Requirements

- Python 3.9 or newer
- scikit-learn
- numpy

## Install and run

```powershell
cd "C:\Users\user\Documents\AiTraining\Task1\financial_tfidf"
python -m pip install -r requirements.txt
python app.py
```

The application lowercases text, normalizes curly apostrophes, splits hyphenated terms, removes English stop words, preserves financial terminology, prints the top 15 terms by maximum TF-IDF, explanations, the complete matrix rounded to four decimals, and a TF-IDF explanation.
