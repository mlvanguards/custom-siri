# Siri Function Calling Dataset

This dataset contains 4500+ examples of local assistant queries mapped to function-calling outputs, following the format used in [Salesforce/xlam-function-calling-60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k).

Example format:

```json
{
  "query": "Open Spotify",
  "answers": "[{\"name\": \"open_application\", \"arguments\": {\"app_name\": \"Spotify\"}}]",
  "tools": "[{\"name\": \"open_application\", \"description\": \"Opens an application\", \"parameters\": {\"app_name\": {\"description\": \"The name of the app\", \"type\": \"str\"}}}]"
}
