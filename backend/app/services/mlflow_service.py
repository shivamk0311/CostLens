import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")

mlflow.set_experiment("Semantic Cache Tuning")

def log_cache_experiment(
        threshold: float,
        similarity_score: float,
        cache_hit: bool,
        latency_ms: float,
        estimated_cost: float,
):
    
    with mlflow.start_run():

        mlflow.log_param("similarity_threshold", threshold)

        mlflow.log_metric("similarity_score", similarity_score)
        mlflow.log_metric("cache hit", int(cache_hit))
        mlflow.log_metric("latency_ms", latency_ms)
        mlflow.log_metric("estimated_cost", estimated_cost)