"""
Helper script to automatically generate pydantic models from a swagger spec
"""

import json
import sys
from pathlib import Path
from typing import Any

API_VERSION = "v1.7"
TYPE_MAPPING = {
    "number": "float",
    "integer": "int",
    "boolean": "bool",
    "string": "str",
}


def read_swagger_spec(api_version: str) -> dict[str, Any]:
    # Get path of current file
    current_dir = Path(__file__).parent
    with open(current_dir / "api" / f"{api_version}.json") as f:
        return json.load(f)


def create_pydantic_fields(params: list[Any]) -> None:
    """
    Parses the parameters and prints Pydantic fields that can be used for the filter model

    There's a couple of special cases we need to consider:
    - Params ending with __in are lists, that expects a comma separated list
    - Params starting with _ must be created with Field and serialization_alias
    """
    for param in params:
        # Skip parameters that are not in the query
        if not param["in"] == "query":
            continue

        name = param["name"]

        try:
            vartype = param["type"]
        except KeyError:
            print(f"Missing type for parameter {name}")
            continue

        # Check if name starts with _
        use_serialization_alias = name.startswith("_")

        # Set Python type based on vartype
        vartype = TYPE_MAPPING.get(vartype, "Any")

        # Check if name ends with __in
        if name.endswith("__in") or name.endswith("__not_in"):
            # Set type according to the type. Valid values are FilterStrList and FilterIntList
            if vartype in ["float", "int"]:
                vartype = "FilterIntList"
            elif vartype == "str":
                vartype = "FilterStrList"

        # If name contains 'Date', case sensitive, its like Date or Datetime
        # Check if name contains 'Date'
        if "Date" in name:
            vartype = "DateTime"

        # Print
        if use_serialization_alias:
            print(
                f'    {name[1:]}: {vartype} = Field(default=None, serialization_alias="{name}")'
            )
        else:
            print(f"    {name}: {vartype} | None = None")


if __name__ == "__main__":
    # Read model from CLI we should be handling
    if len(sys.argv) < 2:
        print("Usage: python generate_filter.py <model>")
        exit(1)

    model = sys.argv[1]
    print(model)

    try:
        spec = read_swagger_spec(API_VERSION)
    except FileNotFoundError:
        print(f"File not found: api/{API_VERSION}")
        exit(1)

    # Read path spec if available
    try:
        path_spec = spec["paths"][f"/api/{API_VERSION}/{model}"]
    except KeyError:
        print(f"Path not found: /api/{API_VERSION}/{model}")
        exit(1)

    # Try to get parameters
    try:
        parameters = path_spec["get"]["parameters"]
    except KeyError:
        print(f"Parameters not found: /api/{API_VERSION}/{model}")
        exit(1)

    create_pydantic_fields(parameters)
