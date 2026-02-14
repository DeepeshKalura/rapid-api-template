"""
Extract test cases from Python integration tests for RapidAPI.

This script parses tests/integration/test_api_integration.py and converts
the test cases into a format suitable for RapidAPI testing documentation.
"""

import ast
import json
import re
from pathlib import Path
from typing import Any


def parse_test_file(test_file_path: str) -> list[dict[str, Any]]:
    """Parse the Python test file and extract test cases."""

    with open(test_file_path) as f:
        content = f.read()

    # Parse the AST
    tree = ast.parse(content)

    # Find all constants (test data)
    constants = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    try:
                        if isinstance(node.value, ast.List):
                            value = ast.literal_eval(node.value)
                            constants[target.id] = value
                    except (ValueError, SyntaxError):
                        pass

    # Find all test functions
    test_cases = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(
            "test_"
        ):
            test_case = extract_test_case(node, constants, content)
            if test_case:
                test_cases.append(test_case)

    return test_cases


def extract_test_case(
    func: ast.FunctionDef | ast.AsyncFunctionDef, constants: dict, content: str
) -> dict[str, Any] | None:
    """Extract a single test case from a test function."""

    # Get the docstring
    docstring = ast.get_docstring(func) or ""

    # Get function source - need to handle line numbers properly
    lines = content.split("\n")
    # AST line numbers are 1-indexed, but Python lists are 0-indexed
    start_idx = func.lineno - 1
    end_idx = func.end_lineno
    func_source = "\n".join(lines[start_idx:end_idx])

    # Determine endpoint and method
    endpoint, method = detect_endpoint_and_method(func_source)

    if not endpoint:
        return None

    # Extract payload/parameters
    payload = extract_payload(func_source, constants)

    # Extract expected status code
    status_code = extract_status_code(func_source)

    # Extract assertions
    assertions = extract_assertions(func_source, constants)

    # Create user-friendly name
    name = create_friendly_name(func.name, endpoint, method)

    return {
        "name": name,
        "description": docstring.strip() if docstring else "",
        "endpoint": endpoint,
        "method": method,
        "payload": payload,
        "params": extract_params(func_source, constants) if method == "GET" else None,
        "expected_status": status_code,
        "assertions": assertions,
        "original_test_name": func.name,
    }


def detect_endpoint_and_method(source: str) -> tuple[str | None, str]:
    """Detect the endpoint and HTTP method from test source."""

    # Check for POST
    if "response = await client.post(" in source:
        match = re.search(r'client\.post\(["\']([^"\']+)["\']', source)
        if match:
            return match.group(1), "POST"

    # Check for GET
    if "response = await client.get(" in source:
        match = re.search(r'client\.get\(["\']([^"\']+)["\']', source)
        if match:
            return match.group(1), "GET"

    return None, "GET"


def extract_payload(source: str, constants: dict) -> dict | None:
    """Extract the request payload from test source."""

    # Find payload definition - look for the payload dictionary
    payload_match = re.search(r"payload\s*=\s*(\{[\s\S]*?\})\n\s*response", source)
    if not payload_match:
        return None

    payload_str = payload_match.group(1)
    payload = {}

    # Parse key-value pairs
    # Pattern: "key": value or 'key': value
    kv_pattern = r'["\']([^"\']+)["\']\s*:\s*([^,\n]+)'
    matches = re.findall(kv_pattern, payload_str)

    for key, value_str in matches:
        value_str = value_str.strip()

        # Check if it's a constant reference
        const_match = re.match(r"([A-Z_]+)\b", value_str)
        if const_match and const_match.group(1) in constants:
            payload[key] = constants[const_match.group(1)]
        else:
            # Try to parse the value
            try:
                # Handle lists like "[]"
                if value_str == "[]":
                    payload[key] = []
                elif value_str == "False":
                    payload[key] = False
                elif value_str == "True":
                    payload[key] = True
                else:
                    payload[key] = ast.literal_eval(value_str)
            except (ValueError, SyntaxError):
                payload[key] = value_str

    return payload if payload else None


def extract_params(source: str, constants: dict) -> dict | None:
    """Extract query parameters from test source."""

    # Look for params in the GET call
    params_match = re.search(r"params\s*=\s*\{(.*?)\}", source, re.DOTALL)
    if not params_match:
        return None

    params_str = params_match.group(1)
    params = {}

    # Pattern: "key": CONSTANT[index] or "key": value
    kv_pattern = r'["\']([^"\']+)["\']\s*:\s*([A-Z_]+)?\[?(\d+)?\]?'
    matches = re.findall(kv_pattern, params_str)

    for match in matches:
        if len(match) >= 3:
            key = match[0]
            const_name = match[1] if match[1] else None
            idx = int(match[2]) if match[2] else None

            if const_name and const_name in constants and idx is not None:
                params[key] = constants[const_name][idx]

    return params if params else None


def extract_status_code(source: str) -> int:
    """Extract expected status code from test source."""

    # Check for specific status code assertions
    status_match = re.search(r"assert\s+response\.status_code\s*==\s*(\d+)", source)
    if status_match:
        return int(status_match.group(1))

    # Default to 200
    return 200


def extract_assertions(source: str, constants: dict) -> list[dict]:
    """Extract assertions from test source."""

    assertions = []

    # Find data assertions - data["field"] == value
    data_assertions = re.findall(
        r'assert\s+data\[["\']([^"\']+)["\']\]\s*==?\s*(.+?)(?:\n|$)', source
    )
    for field, expected in data_assertions:
        expected_clean = expected.strip()

        # Try to parse the expected value
        try:
            expected_val = ast.literal_eval(expected_clean)
        except (ValueError, SyntaxError):
            expected_val = expected_clean

        assertions.append({"type": "equals", "field": field, "expected": expected_val})

    # Find assertions about field existence
    existence_assertions = re.findall(r'assert\s+["\']([^"\']+)["\']\s+in\s+data', source)
    for field in existence_assertions:
        assertions.append({"type": "exists", "field": field})

    # Find range assertions (for distances) - assert 3000 < data["distance_nm"] < 5000
    range_matches = re.findall(
        r'assert\s+(\d+)\s*<\s*data\[["\']([^"\']+)["\']\]\s*<\s*(\d+)', source
    )
    for min_val, field, max_val in range_matches:
        assertions.append(
            {"type": "range", "field": field, "min": int(min_val), "max": int(max_val)}
        )

    # Find "in" assertions (for strings) - assert "substring" in data["field"]
    in_assertions = re.findall(
        r'assert\s+["\']([^"\']+)["\']\s+in\s+data\[["\']([^"\']+)["\']\]', source
    )
    for expected_substring, field in in_assertions:
        assertions.append({"type": "contains", "field": field, "expected": expected_substring})

    return assertions


def create_friendly_name(test_name: str, endpoint: str, method: str) -> str:
    """Create a user-friendly name for the test."""

    # Remove test_ prefix and underscores, convert to title case
    name = test_name.replace("test_", "").replace("_", " ").title()

    return f"{name} ({method} {endpoint})"


def generate_rapidapi_test_suite(test_cases: list) -> dict:
    """Generate a test suite in RapidAPI-compatible format."""

    return {
        "test_suite": {
            "name": "Ecomarine API Test Suite",
            "description": "Automated test cases extracted from Python integration tests",
            "version": "1.0.0",
            "created_at": "{{timestamp}}",
            "tests": test_cases,
        }
    }


def generate_markdown_documentation(test_cases: list) -> str:
    """Generate markdown documentation for the test cases."""

    md = "# Ecomarine API Test Cases\n\n"
    md += "This document contains all test cases extracted from Python integration tests.\n\n"
    md += "## Test Summary\n\n"
    md += f"- **Total Tests**: {len(test_cases)}\n"

    # Group by endpoint
    by_endpoint = {}
    for test in test_cases:
        ep = test["endpoint"]
        if ep not in by_endpoint:
            by_endpoint[ep] = []
        by_endpoint[ep].append(test)

    md += f"- **Endpoints Covered**: {len(by_endpoint)}\n"
    md += "\n## Tests by Endpoint\n\n"

    for endpoint, tests in by_endpoint.items():
        md += f"### {endpoint}\n\n"
        for i, test in enumerate(tests, 1):
            md += f"{i}. **{test['name']}**\n"
            if test["description"]:
                md += f"   - Description: {test['description']}\n"
            md += f"   - Method: {test['method']}\n"
            md += f"   - Expected Status: {test['expected_status']}\n"
            if test["payload"]:
                md += f"   - Payload: `{json.dumps(test['payload'], indent=2)}`\n"
            if test["params"]:
                md += f"   - Params: `{json.dumps(test['params'], indent=2)}`\n"
            md += "\n"

    return md


def generate_curl_commands(test_cases: list) -> dict:
    """Generate curl commands for each test case."""

    commands = {}
    base_url = "https://your-api-url.rapidapi.com"

    for test in test_cases:
        if test["method"] == "POST":
            curl = f"""curl -X POST "{base_url}{test["endpoint"]}" \\
-H "Content-Type: application/json" \\
-H "X-RapidAPI-Key: YOUR_API_KEY" \\
-H "X-RapidAPI-Host: your-api-host.rapidapi.com" \\
-d '{json.dumps(test.get("payload", {}))}'"""
        else:
            params = ""
            if test.get("params"):
                params = "?" + "&".join([f"{k}={v}" for k, v in test["params"].items()])

            curl = f"""curl "{base_url}{test["endpoint"]}{params}" \\
-H "X-RapidAPI-Key: YOUR_API_KEY" \\
-H "X-RapidAPI-Host: your-api-host.rapidapi.com"""

        commands[test["name"]] = {
            "curl": curl,
            "expected_status": test["expected_status"],
            "assertions": test["assertions"],
        }

    return commands


if __name__ == "__main__":
    # Parse the test file (from project root)
    project_root = Path(__file__).parent.parent
    test_file = project_root / "tests" / "integration" / "test_api_integration.py"

    if not test_file.exists():
        print(f"Error: Test file not found at {test_file}")
        exit(1)

    print("🔍 Parsing Python integration tests...")
    test_cases = parse_test_file(str(test_file))

    print(f"✅ Extracted {len(test_cases)} test cases")

    # Generate outputs
    outputs_dir = project_root / ".rapidapi" / "tests"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # 1. JSON test suite
    test_suite = generate_rapidapi_test_suite(test_cases)
    with open(outputs_dir / "test_suite.json", "w") as f:
        json.dump(test_suite, f, indent=2)
    print(f"📄 Generated: {outputs_dir / 'test_suite.json'}")

    # 2. Markdown documentation
    markdown = generate_markdown_documentation(test_cases)
    with open(outputs_dir / "test_cases.md", "w") as f:
        f.write(markdown)
    print(f"📄 Generated: {outputs_dir / 'test_cases.md'}")

    # 3. Curl commands
    curl_commands = generate_curl_commands(test_cases)
    with open(outputs_dir / "curl_commands.json", "w") as f:
        json.dump(curl_commands, f, indent=2)
    print(f"📄 Generated: {outputs_dir / 'curl_commands.json'}")

    # 4. Summary
    summary = {
        "total_tests": len(test_cases),
        "endpoints": list({t["endpoint"] for t in test_cases}),
        "test_names": [t["name"] for t in test_cases],
    }
    with open(outputs_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n✨ Test extraction complete!")
    print(f"   - Total tests: {len(test_cases)}")
    print(f"   - Endpoints: {len(summary['endpoints'])}")
    print(f"   - Output directory: {outputs_dir}")
