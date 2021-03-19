class GraphQL:
    @staticmethod
    def content(results):
        all_results = []
        for category in results:
            all_results.extend(results[category])

        return [{**row, "owner": row["owner"]["name"]} for row in all_results]

    @staticmethod
    def tags(results):
        print(results)
        all_results = []
        for tag in results["tags"]:
            for wb in tag["workbooks"]:
                all_results.append({"content_id": wb["luid"], "tag": tag["name"]})

            for ds in tag["datasources"]:
                all_results.append({"content_id": ds["luid"], "tag": tag["name"]})

        return all_results

