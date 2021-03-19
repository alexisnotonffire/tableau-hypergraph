class GraphQL:
    @staticmethod
    def content(results):
        all_results = []
        for content_type, contents in results.items():
            for content in contents:
                all_results.append(
                    {
                        **content,
                        "owner": content["owner"]["name"],
                        "content_type": content_type
                    }
                )

        transform = lambda x: [
            x["content_type"],
            x["luid"],
            x["name"],
            x["owner"],
            x["projectName"],
            x["description"],
        ]
        return map(transform, all_results)

    @staticmethod
    def tags(results):
        all_results = []
        for tag in results["tags"]:
            for wb in tag["workbooks"]:
                all_results.append({"content_id": wb["luid"], "tag": tag["name"]})

            for ds in tag["datasources"]:
                all_results.append({"content_id": ds["luid"], "tag": tag["name"]})

        transform = lambda x: [
            x["content_id"],
            x["tag"]
        ]
        return map(transform, all_results)

    @staticmethod
    def content_dependencies(results):
        all_results = []
        for ds in results["publishedDatasources"]:
            for wb in ds["downstreamWorkbooks"]:
                all_results.append({"upstream_content_id": ds["luid"], "downstream_content_id": wb["luid"]})

        transform = lambda x: [
            x["upstream_content_id"],
            x["downstream_content_id"]
        ]
        return map(transform, all_results)

    @staticmethod
    def database_dependencies(results):
        all_results = []
        location = None
        location_options = [
            "hostName",
            "filePath",
            "fileId"
        ]
        for ds in results["databases"]:
            for option in location_options:
                location = ds.get(option)
                if location:
                    break

            row = {
                "database": ds["name"],
                "location": location,
                "type": ds["connectionType"]
            }

            for wb in ds["downstreamWorkbooks"]:
                all_results.append({
                    "upstream_content_id": wb["luid"],
                    **row
                })

            for pds in ds["downstreamDatasources"]:
                all_results.append({
                    "upstream_content_id": pds["luid"],
                    **row
                })

        transform = lambda x: [
            x["upstream_content_id"],
            x["location"],
            x["database"],
            x["type"]
        ]
        return map(transform, all_results)

