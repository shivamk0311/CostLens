import csv
import os
from collections import defaultdict

import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
load_dotenv("backend/.env")


CSV_PATH = "CostLens_Semantic_Cache_Benchmark_250 (1).csv"

THRESHOLDS = [
    0.55,
    0.58,
    0.60,
    0.62,
    0.64,
    0.65,
    0.66,
    0.67,
    0.68,
    0.70
]


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def generate_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return {
        text: np.array(item.embedding)
        for text, item in zip(texts, response.data)
    }


def main():
    rows = load_rows()

    unique_texts = set()

    for row in rows:
        unique_texts.add(row["prompt"])

        if row["reference_seed"]:
            unique_texts.add(row["reference_seed"])

    unique_texts = list(unique_texts)

    print(
        f"Generating embeddings for "
        f"{len(unique_texts)} unique prompts..."
    )

    embeddings = {}

    batch_size = 100

    for i in range(0, len(unique_texts), batch_size):
        batch = unique_texts[i:i + batch_size]

        batch_embeddings = generate_embeddings(batch)

        embeddings.update(batch_embeddings)

        print(
            f"Embedded "
            f"{min(i + batch_size, len(unique_texts))}"
            f"/{len(unique_texts)}"
        )

    examples = []

    for row in rows:
        case_type = row["case_type"]

        if case_type == "seed":
            continue

        if case_type == "exact_duplicate":
            continue

        prompt = row["prompt"]
        reference_seed = row["reference_seed"]

        if not reference_seed:
            reference_seed = next(
                r["prompt"]
                for r in rows
                if r["group_id"] == row["group_id"]
                and r["case_type"] == "seed"
            )

        similarity = cosine_similarity(
            embeddings[prompt],
            embeddings[reference_seed]
        )

        should_reuse = (
            row["should_reuse_cache"].lower()
            == "true"
        )

        examples.append({
            "group_id": row["group_id"],
            "case_type": case_type,
            "prompt": prompt,
            "similarity": similarity,
            "should_reuse": should_reuse,
        })

    positives = [
        x["similarity"]
        for x in examples
        if x["should_reuse"]
    ]

    negatives = [
        x["similarity"]
        for x in examples
        if not x["should_reuse"]
    ]

    print("\n==============================")
    print("SIMILARITY DISTRIBUTION")
    print("==============================")

    print(
        f"Positive examples: {len(positives)}"
    )

    print(
        f"Negative examples: {len(negatives)}"
    )

    print(
        f"Positive avg similarity: "
        f"{np.mean(positives):.4f}"
    )

    print(
        f"Positive min similarity: "
        f"{np.min(positives):.4f}"
    )

    print(
        f"Positive max similarity: "
        f"{np.max(positives):.4f}"
    )

    print(
        f"Negative avg similarity: "
        f"{np.mean(negatives):.4f}"
    )

    print(
        f"Negative min similarity: "
        f"{np.min(negatives):.4f}"
    )

    print(
        f"Negative max similarity: "
        f"{np.max(negatives):.4f}"
    )

    print("\n==============================")
    print("THRESHOLD EVALUATION")
    print("==============================")

    best = None

    for threshold in THRESHOLDS:
        tp = 0
        fp = 0
        tn = 0
        fn = 0

        for item in examples:
            predicted_reuse = (
                item["similarity"] >= threshold
            )

            actual_reuse = item["should_reuse"]

            if predicted_reuse and actual_reuse:
                tp += 1

            elif predicted_reuse and not actual_reuse:
                fp += 1

            elif not predicted_reuse and not actual_reuse:
                tn += 1

            elif not predicted_reuse and actual_reuse:
                fn += 1

        precision = (
            tp / (tp + fp)
            if (tp + fp)
            else 0
        )

        recall = (
            tp / (tp + fn)
            if (tp + fn)
            else 0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if (precision + recall)
            else 0
        )

        print(
            f"Threshold={threshold:.2f} | "
            f"Precision={precision:.3f} | "
            f"Recall={recall:.3f} | "
            f"F1={f1:.3f} | "
            f"TP={tp} FP={fp} "
            f"TN={tn} FN={fn}"
        )

        if best is None or f1 > best["f1"]:
            best = {
                "threshold": threshold,
                "precision": precision,
                "recall": recall,
                "f1": f1,
            }

    print("\n==============================")
    print("BEST THRESHOLD")
    print("==============================")

    print(
        f"Threshold: {best['threshold']:.2f}"
    )

    print(
        f"Precision: {best['precision']:.3f}"
    )

    print(
        f"Recall: {best['recall']:.3f}"
    )

    print(
        f"F1: {best['f1']:.3f}"
    )

    print("\nLowest positive similarities:")

    for item in sorted(
        [
            x
            for x in examples
            if x["should_reuse"]
        ],
        key=lambda x: x["similarity"]
    )[:10]:
        print(
            f"{item['similarity']:.4f} | "
            f"{item['group_id']} | "
            f"{item['prompt']}"
        )

    print("\nHighest negative similarities:")

    for item in sorted(
        [
            x
            for x in examples
            if not x["should_reuse"]
        ],
        key=lambda x: x["similarity"],
        reverse=True
    )[:10]:
        print(
            f"{item['similarity']:.4f} | "
            f"{item['group_id']} | "
            f"{item['prompt']}"
        )


if __name__ == "__main__":
    main()