def flatten_results(results):
    all_results = []
    for category in results:
        all_results.extend(results[category])

    return [{**row, "owner": row["owner"]["name"]} for row in all_results]
