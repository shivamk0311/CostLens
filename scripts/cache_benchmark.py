import csv
import time
import requests
from statistics import mean

API_URL = "http://localhost:8000/v1/chat/completions"
CSV_PATH = "CostLens_Semantic_Cache_Benchmark_250 (1).csv"


def run_benchmark():
    total_requests = 0
    cache_hits = 0
    exact_hits = 0
    semantic_hits = 0

    latencies = []
    cache_hit_latencies = []
    cache_miss_latencies = []

    estimated_cost = 0.0

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            payload = {
                "model": row["model"],
                "messages": [
                    {
                        "role": "user",
                        "content": row["prompt"]
                    }
                ],
                "temperature": float(row["temperature"])
            }

            headers = {
                "X-CostLens-Feature": row["feature"]
            }

            start = time.perf_counter()

            response = requests.post(
                API_URL,
                json=payload,
                headers=headers,
                timeout=60
            )

            elapsed_ms = (time.perf_counter() - start) * 1000

            total_requests += 1
            latencies.append(elapsed_ms)

            if response.status_code != 200:
                print(
                    f"[{row['request_id']}] FAILED "
                    f"{response.status_code}: {response.text}"
                )
                continue

            data = response.json()
            
            # print("RAW RESPONSE:", data)
            # if elapsed_ms < 1000:
            #     print("FAST RESPONSE:", data)
            
            costlens = data.get("costlens", {})

            cache_hit = costlens.get("cache_hit", False)
            cache_type = costlens.get("cache_type")
            # print(cache_type = costlens.get("cache_type"))

            if cache_hit:
                cache_hits += 1
                cache_hit_latencies.append(elapsed_ms)

                print("COSTLENS RESPONSE:", costlens)

                if cache_type == "exact":
                    exact_hits += 1

                elif cache_type == "semantic":
                    semantic_hits += 1
                else:
                    print(
                        f"WARNING: cache hit with unknown cache type: "
                        f"{cache_type}"
                    )

            else:
                cache_miss_latencies.append(elapsed_ms)

                estimated_cost += costlens.get(
                    "estimated_cost_usd",
                    0
                )

            print(
                f"[{row['request_id']}] "
                f"cache_hit={cache_hit} "
                f"type={cache_type} "
                f"latency={elapsed_ms:.2f} ms"
            )

    hit_rate = (
        cache_hits / total_requests * 100
        if total_requests
        else 0
    )

    avg_latency = mean(latencies) if latencies else 0

    avg_hit_latency = (
        mean(cache_hit_latencies)
        if cache_hit_latencies
        else 0
    )

    avg_miss_latency = (
        mean(cache_miss_latencies)
        if cache_miss_latencies
        else 0
    )

    latency_reduction = 0

    if avg_miss_latency > 0:
        latency_reduction = (
            (avg_miss_latency - avg_hit_latency)
            / avg_miss_latency
            * 100
        )

    print("\n==============================")
    print("COSTLENS CACHE BENCHMARK")
    print("==============================")

    print(f"Total requests: {total_requests}")
    print(f"Cache hits: {cache_hits}")
    print(f"Exact hits: {exact_hits}")
    print(f"Semantic hits: {semantic_hits}")
    print(f"Cache hit rate: {hit_rate:.2f}%")

    print(f"Average latency: {avg_latency:.2f} ms")
    print(f"Average hit latency: {avg_hit_latency:.2f} ms")
    print(f"Average miss latency: {avg_miss_latency:.2f} ms")

    print(
        f"Latency reduction on cached requests: "
        f"{latency_reduction:.2f}%"
    )

    print(
        f"Observed API cost on misses: "
        f"${estimated_cost:.6f}"
    )


if __name__ == "__main__":
    run_benchmark()