"""TF-IDF analysis for eight financial-domain documents."""
import re
import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

DOCUMENTS = [
    ("Transaction Analysis", "The customer’s checking account shows a $12,500 incoming wire transfer followed by three international transfers totaling $11,800 within 24 hours."),
    ("Loan Assessment", "The applicant has a monthly income of ₹180,000, existing loan obligations of ₹45,000 per month, and a requested personal loan of ₹2,000,000."),
    ("Fraud Detection", "A credit card transaction of ₹275,000 was initiated from Mumbai while the customer’s previous transaction, made 20 minutes earlier, occurred in Bengaluru."),
    ("Investment Analysis", "The portfolio contains 40% large-cap equities, 30% government bonds, 20% corporate bonds, and 10% cash, with an investment horizon of five years."),
    ("Credit Risk", "The borrower’s credit score decreased from 780 to 690 after two missed credit-card payments during the previous six months."),
    ("KYC/Compliance", "The customer has provided a passport and proof of address, but the beneficial owner of the associated business has not yet been verified."),
    ("Market Analysis", "The company’s quarterly revenue increased by 18% year over year, while operating expenses increased by 27%, resulting in a decline in operating margin."),
    ("Payment Reconciliation", "The accounting system reports 1,250 payments for the day, while the bank statement contains 1,238 corresponding transactions, leaving 12 payments requiring reconciliation."),
]


def preprocess(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"(?<=\w)'(?=\w)", "", text)
    text = re.sub(r"[-‐‑‒–—]", " ", text)
    return text.lower()


def main():
    categories = [category for category, _ in DOCUMENTS]
    texts = [text for _, text in DOCUMENTS]
    vectorizer = TfidfVectorizer(
        preprocessor=preprocess,
        lowercase=False,
        stop_words="english",
        token_pattern=r"(?u)(?<!\w)(?:[$₹]\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?%?|[a-zA-Z][a-zA-Z0-9_]*)(?!\w)",
    )
    matrix = vectorizer.fit_transform(texts)
    terms = vectorizer.get_feature_names_out()
    values = matrix.toarray()
    max_scores = values.max(axis=0)
    max_docs = values.argmax(axis=0)
    ranked = sorted(range(len(terms)), key=lambda i: (-max_scores[i], terms[i]))[:15]

    assert len(ranked) == 15
    assert all(np.isfinite(max_scores[i]) for i in ranked)
    assert all(max_scores[ranked[i]] >= max_scores[ranked[i + 1]] for i in range(14))

    print("=" * 110)
    print("FINANCIAL-DOMAIN TF-IDF ANALYSIS")
    print("=" * 110)
    print("Specialness = maximum TF-IDF score across all 8 documents\n")
    print("A. TOP 15 MOST DISTINCTIVE WORDS")
    print(f"{'Rank':<6}{'Word':<22}{'TF-IDF':<12}{'Document':<12}Category")
    print("-" * 110)
    for rank, i in enumerate(ranked, 1):
        doc = max_docs[i]
        print(f"{rank:<6}{terms[i]:<22}{max_scores[i]:<12.4f}{doc + 1:<12}{categories[doc]}")

    print("\nB. EXPLANATION FOR EACH TOP-15 WORD")
    for rank, i in enumerate(ranked, 1):
        doc = max_docs[i]
        frequency = int((values[:, i] > 0).sum())
        reason = (f"It appears only in document {doc + 1}." if frequency == 1 else f"It appears in {frequency} documents and is most important in this document.")
        print(f"\n{rank}. Word: {terms[i]}")
        print(f"   TF-IDF score: {max_scores[i]:.4f}")
        print(f"   Document: {doc + 1} | Category: {categories[doc]}")
        print(f"   Original sentence: {DOCUMENTS[doc][1]}")
        print(f"   Why distinctive: {reason}")

    print("\nC. COMPLETE TF-IDF MATRIX")
    print("Rows are documents; columns are vocabulary terms.")
    print("\t".join(["Document"] + list(terms)))
    for doc, row in enumerate(values):
        print("\t".join([f"{doc + 1}: {categories[doc]}"] + [f"{x:.4f}" for x in row]))

    print("\nD. TF-IDF EXPLANATION")
    print("Term Frequency (TF) measures how often a term occurs in a document.")
    print("Inverse Document Frequency (IDF) gives more weight to terms found in fewer documents.")
    print("TF-IDF is TF multiplied by IDF; a high value indicates a term is important in one document and uncommon overall.")
    print("\nValidation: exactly 15 results, numeric scores, descending order, and valid document/category mappings.")


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        raise RuntimeError("Python 3.9 or newer is required.")
    main()
