from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def experiment_1():
    print("\n=== Experiment 1: Basic embedding ===")
    text = "The cat is sleeping."
    embedding = model.encode(text)
    print(f"Embedding dimension: {embedding.shape}")
    print(f"First 10 values: {embedding[:10]}")


def experiment_2():
    print("\n=== Experiment 2: Similar sentences ===")
    a = "The cat is sleeping."
    b = "A kitten is taking a nap."
    c = "The stock market fell today."

    emb_a = model.encode(a)
    emb_b = model.encode(b)
    emb_c = model.encode(c)

    sim_ab = cos_sim(emb_a, emb_b).item()
    sim_ac = cos_sim(emb_a, emb_c).item()

    print(f"similarity(A, B) = {sim_ab:.4f}")
    print(f"similarity(A, C) = {sim_ac:.4f}")
    print(f"A,B > A,C ? {sim_ab > sim_ac}")


def experiment_3():
    print("\n=== Experiment 3: Paraphrases ===")
    sentences = [
        "The model detects humans.",
        "The system identifies people.",
        "The algorithm recognizes human objects.",
    ]
    embeddings = model.encode(sentences)
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            sim = cos_sim(embeddings[i], embeddings[j]).item()
            print(f"sim('{sentences[i]}', '{sentences[j]}') = {sim:.4f}")


def experiment_4():
    print("\n=== Experiment 4: Keyword trap ===")
    a = "Apple released a new computer."
    b = "Apple is a fruit that grows on trees."
    c = "Microsoft released a new laptop."

    emb_a = model.encode(a)
    emb_b = model.encode(b)
    emb_c = model.encode(c)

    sim_ab = cos_sim(emb_a, emb_b).item()
    sim_ac = cos_sim(emb_a, emb_c).item()

    print(f"similarity(Apple-computer, Apple-fruit) = {sim_ab:.4f}")
    print(f"similarity(Apple-computer, Microsoft-laptop) = {sim_ac:.4f}")

import json
import time


def experiment_5():
    print("\n=== Experiment 5: Real chunks ===")
    with open("data/chunks/attention-is-all-you-need.json") as f:
        chunks = json.load(f)[:30]  # take first 30

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts)

    for c, emb in zip(chunks, embeddings):
        print(f"{c['chunk_id']} | tokens={c['token_count']} | dim={emb.shape[0]}")

def compare_models():
    print("\n=== Model comparison ===")
    with open("data/chunks/attention-is-all-you-need.json") as f:
        chunks = json.load(f)[:50]
    texts = [c["text"] for c in chunks]

    models_to_test = {
        "BGE-small": "BAAI/bge-small-en-v1.5",
        "E5-small": "intfloat/e5-small-v2",
    }

    results = []
    for name, model_id in models_to_test.items():
        m = SentenceTransformer(model_id)
        start = time.time()
        embeddings = m.encode(texts)
        elapsed = time.time() - start

        results.append({
            "name": name,
            "dimension": embeddings.shape[1],
            "total_time": elapsed,
            "avg_time_per_chunk": elapsed / len(texts),
        })

    print(f"{'Model':<15}{'Dimension':<12}{'Total Time':<15}{'Avg/Chunk':<12}")
    for r in results:
        print(f"{r['name']:<15}{r['dimension']:<12}{r['total_time']:.3f}s{'':<9}{r['avg_time_per_chunk']*1000:.1f}ms")

if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()
    experiment_5()
    compare_models()