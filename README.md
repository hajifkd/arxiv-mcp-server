# Yet another arxiv mcp server
This is a simple mcp server that uses the arxiv API to get the latest papers in a given category.
The API is kept as simple as possible, so that LLMs can easily use it.

## Running the server
```bash
# Run the server directly
uvx --from git+https://github.com/hajifkd/arxiv-mcp-server arxiv-mcp-server
```

## Test APIs
It seems that there's no way to easily do unit tests for mcp APIs.
The best way to test them is to run the inspector and check the output.
```bash
uv pip install -e .
npx @modelcontextprotocol/inspector arxiv-mcp-server
```

