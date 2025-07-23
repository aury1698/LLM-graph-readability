curl https://aqueduct.ai.datalab.tuwien.ac.at/chat/completions \
  -H "Authorization: Bearer $AQUEDUCT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-32b",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write me a short poem!"}
    ]
  }'
