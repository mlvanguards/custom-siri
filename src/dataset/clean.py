import torch
from sentence_transformers import SentenceTransformer, util


def deduplicate_and_decontaminate_dataset(
    dataset, reference_queries=[], similarity_threshold=0.85
):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    clean_dataset = []
    seen_embeddings = []

    ref_embeddings = (
        model.encode(
            reference_queries, convert_to_tensor=True, normalize_embeddings=True
        )
        if reference_queries
        else None
    )

    for entry in dataset:
        query = entry.get("query", "").strip()
        if len(query) < 5:
            continue

        query_embedding = model.encode(
            query, convert_to_tensor=True, normalize_embeddings=True
        )

        if seen_embeddings:
            similarities = util.pytorch_cos_sim(
                query_embedding, torch.stack(seen_embeddings)
            )
            if torch.any(similarities > similarity_threshold):
                continue

        if ref_embeddings is not None:
            ref_similarities = util.pytorch_cos_sim(query_embedding, ref_embeddings)
            if torch.any(ref_similarities > similarity_threshold):
                continue

        seen_embeddings.append(query_embedding)
        clean_dataset.append(entry)

    return clean_dataset
