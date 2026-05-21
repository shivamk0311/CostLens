from app.models.semantic_cache import SemanticCache
import json
import hashlib

def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

def find_exact_cache_match(db, prompt):
    prompt_hash = hash_prompt(prompt)

    return (db.query(SemanticCache).filter(SemanticCache.prompt_hash == prompt_hash).first())

def store_cache_entry(db, prompt, embedding, response:dict):

    cache_entry = SemanticCache(
        prompt = prompt,
        prompt_hash = hash_prompt(prompt),
        embedding = embedding,
        response = json.dumps(response),
        hit_count = 0,
    )

    db.add(cache_entry)
    db.commit()
    db.refresh(cache_entry)

    return cache_entry


def increment_cache_hit(db, cache_entry):
    cache_entry.hit_count += 1
    db.commit()
    db.refresh(cache_entry)

    return cache_entry