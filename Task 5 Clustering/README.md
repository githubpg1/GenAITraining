# Financial NLP: Word2Vec, Similarity, Clustering, and PCA

This project analyzes exactly 25 financial-domain sentences using preprocessing, gensim Word2Vec, semantic similarity, averaged sentence embeddings, KMeans clustering, PCA, and a seaborn scatter plot.

## Requirements

Python 3.9+ and the packages in `requirements.txt`.

## Install and run

```powershell
cd "C:\Users\user\Documents\AiTraining\Task1\financial_nlp"
python -m pip install -r requirements.txt
python main.py
```

The script uses the same dataset from `data/financial_sentences.txt` throughout the pipeline. It saves `financial_clusters_pca.png` in the project directory. Word2Vec results are educational because the model is trained on only 25 sentences.
