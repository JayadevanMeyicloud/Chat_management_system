import re


class Router:
    def __init__(self):
        self.routes = []

    def get(self, path):
        return self._register("GET", path)

    def post(self, path):
        return self._register("POST", path)

    def put(self, path):
        return self._register("PUT", path)

    def patch(self, path):
        return self._register("PATCH", path)

    def delete(self, path):
        return self._register("DELETE", path)

    def _register(self, method, path):

        def decorator(func):
            pattern = self._convert_path_to_regex(path)
            self.routes.append(
                {
                    "method": method,
                    "path": path,
                    "pattern": re.compile(f"^{pattern}$"),
                    "handler": func,
                }
            )
            return func

        return decorator

    def _convert_path_to_regex(self, path):
        """
        Converts:

        /users/{id}

        into:

        /users/(?P<id>[^/]+)

        """

        return re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)

    def resolve(self, event, context):

        method = event.get("httpMethod")

        path = event.get("path", "")

        for route in self.routes:
            # Check HTTP method

            if route["method"] != method:
                continue

            # Check path match

            match = route["pattern"].match(path)

            if match:
                path_params = match.groupdict()

                return route["handler"](event, context, **path_params)

        return {"statusCode": 404, "body": "Route not found"}
