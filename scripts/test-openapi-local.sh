#!/bin/bash
# Test OpenAPI spec generation locally
# This simulates what the CI/CD workflow does

echo "🧪 Testing OpenAPI Spec Generation Locally"
echo "============================================"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found"
    echo "Please run this script from the repository root"
    exit 1
fi

echo "✅ Found main.py"
echo ""

# Install dependencies if needed
echo "📦 Checking dependencies..."
if ! command -v uv &> /dev/null; then
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "Running uv sync..."
uv sync

# Start FastAPI server in background
echo ""
echo "🚀 Starting FastAPI server..."
uv run uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to be ready
echo ""
echo "⏳ Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Server is ready!"
        break
    fi
    echo "  Attempt $i/30..."
    sleep 2
done

# Test health endpoint
echo ""
echo "🔍 Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/)
echo "Response: $HEALTH"

# Generate OpenAPI JSON
echo ""
echo "📄 Generating OpenAPI JSON..."
curl -s http://localhost:8000/openapi.json | python -m json.tool > test_openapi.json

if [ -s test_openapi.json ]; then
    echo "✅ OpenAPI JSON generated successfully"
    echo "📊 Size: $(wc -c < test_openapi.json) bytes"
    echo ""
    echo "Preview (first 30 lines):"
    head -30 test_openapi.json
else
    echo "❌ Failed to generate OpenAPI JSON"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Generate YAML version
echo ""
echo "📄 Converting to YAML..."
uv run python -c "
import json
import yaml
with open('test_openapi.json', 'r') as f:
    data = json.load(f)
with open('test_openapi.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)
print('✅ OpenAPI YAML generated')
"

# Show summary
echo ""
echo "📊 Summary"
echo "=========="
echo "JSON file: test_openapi.json ($(wc -c < test_openapi.json) bytes)"
echo "YAML file: test_openapi.yaml ($(wc -c < test_openapi.yaml) bytes)"
echo ""

# List endpoints
echo "🎯 Endpoints found:"
uv run python -c "
import json
with open('test_openapi.json', 'r') as f:
    spec = json.load(f)
for path, methods in spec.get('paths', {}).items():
    for method in methods.keys():
        if method != 'parameters':
            print(f'  {method.upper():6} {path}')
"

# Cleanup
echo ""
echo "🧹 Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "✅ Test complete!"
echo ""
echo "Files generated:"
echo "  - test_openapi.json"
echo "  - test_openapi.yaml"
echo ""
echo "To clean up test files: rm test_openapi.json test_openapi.yaml"
