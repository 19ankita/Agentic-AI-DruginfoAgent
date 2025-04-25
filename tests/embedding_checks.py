from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = model.encode("I had severe fatigue during treatment.")
print(embedding.shape)  # Should be (384,)
