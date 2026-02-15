# Build your own Siri

![Build your own Siri](images/BYOS.webp)

A complete pipeline for building your own Siri-like voice assistant that runs entirely locally. This project includes dataset generation, model fine-tuning, and a real-time inference system with both voice and text input capabilities. This project is the implementation of the solution described in the [4+1 part course: Build your own Siri, by Hyperplane](https://thehyperplane.substack.com/p/build-your-own-siri-locally-on-device).

![Build your own Siri workflow](images/build_siri.webp)

## Table of Contents
* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Dataset Generation](#dataset-generation)
* [Available Functions](#available-functions)
* [Project Structure](#project-structure)
* [Development](#development)
* [License](#license)

## Overview

This project implements a complete pipeline for building a local voice assistant, from dataset generation to model deployment. 

**Dataset Generation Process:**
* Uses Salesforce's xlam-function-calling-60k dataset as few-shot prompt foundation
* Generates fresh, paraphrased examples with human-like responses
* Removes unnecessary data, focusing on quality enhancement
* Creates realistic function-calling scenarios in ShareGPT format

**Model Selection & Training:**
* **Comparative evaluation**: LLaMA 3.1 8B Instruct vs Gemma 2 2B
* **Winner**: LLaMA 3.1 achieved **100% JSON validity and 100% function call accuracy** vs Gemma 2's 70%
* **Fine-tuning strategy**: LoRA (r=16, α=16) with Unsloth for 2-5x faster training
* **Training setup**: 3 epochs, lr=2e-4, batch size 8, W&B logging

**Deployment & Quantization:**
* **Model quantization**: GGUF format with q4_k_m, q5_k_m, q8_0 variants
* **Real-time inference**: Optimized for edge deployment with 4.8GB model size
* **Cross-platform support**: Windows, macOS, Linux compatibility

**Edge integration:(coming soon)**

## Features

* **Complete ML Pipeline**: End-to-end system from dataset generation to model deployment
* **Superior Performance**: 100% JSON validity and function call accuracy with LLaMA 3.1 (vs 70% for Gemma 2)
* **Dual Input Methods**: Voice recording with Whisper STT + text input alternative
* **Optimized Training**: Unsloth integration for 2-5x faster fine-tuning with LoRA
* **Interactive Demo**: Streamlit interface for real-time testing and validation
* **Cross-platform**: Windows, macOS, Linux support with platform-specific optimizations
* **Multiple Model Variants**: q4_k_m (4.8GB), q5_k_m, q8_0 quantized versions
* **Edge deployment**: **Coming soon**

## Key Technical Achievements

**Model Evaluation Results:**
* **LLaMA 3.1 8B**: 100% JSON validity, 100% function call accuracy
* **Gemma 2 2B**: 70% JSON validity, 70% function call accuracy
* **Dataset Quality**: Custom dataset based on Salesforce's xlam-function-calling-60k
* **Training Efficiency**: 3 epochs with LoRA fine-tuning using Unsloth optimization

**Architecture Highlights:**
* **LoRA Configuration**: rank=16, alpha=16, targeting attention and MLP layers
* **Training Setup**: batch_size=8, lr=2e-4, gradient_accumulation_steps=2
* **Quantization Strategy**: Multiple GGUF variants for different hardware constraints
* **Real-world Validation**: Streamlit interface for comprehensive testing

## Prerequisites

* Python 3.12 or higher
* uv (for dependency management)
* CUDA-capable GPU (recommended for training)
* Microphone for voice input
* 8GB+ RAM

## Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/custom-siri.git
cd custom-siri
```

2. Install dependencies:
```bash
uv sync
```

3. Activate virtual environment:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Docker Setup
Build and run using Docker:

```bash
docker build -t custom-siri .
docker run -p 8501:8501 --rm custom-siri \
```

### Example Commands

**Voice/Text Input:**
* *"Set the volume to 50 and search for Python tutorials"*
* *"Take a screenshot and create a folder called Projects"*
* *"Open Chrome and show me the battery status"*
* *"Lock the screen and pause the music"*

## Dataset Generation

This project includes a comprehensive dataset generation pipeline that creates high-quality function-calling examples for training the Siri assistant. The pipeline generates diverse conversational examples across multiple categories.

### Prerequisites

Before generating datasets, ensure you have:

1. **Ollama installed and running**: The generation process uses Ollama for LLM inference
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   ollama serve
   ollama pull llama3.1:8b  # or your preferred model
   ```

2. **Environment Configuration**: Set up your environment variables in `.env` (optional):
   ```bash
   # Optional: For Hugging Face dataset uploads
   HUGGINGFACE_TOKEN=your_token_here
   
   # Optional: For OpenAI API (if using OpenAI models)
   OPENAI_API_KEY=your_key_here
   ```

3. **Model Configuration**: Edit `settings.py` to configure your preferred model:
   ```python
   # Available models in DatasetSettings:
   LLM_MODEL = "ollama/llama3.1:8b"      # Default (recommended)
   # LLM_MODEL = "ollama/gemma2:9b"       # Alternative
   # LLM_MODEL = "ollama/llama3.2:3b"     # Smaller/faster
   # LLM_MODEL = "ollama/qwen2.5:7b"      # Alternative
   ```

### Dataset Generation Process

The pipeline generates four types of examples:

1. **Single Tool Examples**: Individual function calls with natural language queries
2. **Multi-Tool Examples**: Complex scenarios requiring multiple function calls
3. **Unknown Intent Examples**: Queries that cannot be fulfilled by available functions
4. **Adversarial Examples**: Edge cases and challenging scenarios
5. **Paraphrased Examples**: Variations of existing examples for data augmentation

### Usage

#### Basic Dataset Generation

Generate a dataset with default parameters (recommended for testing):

```bash
cd src/dataset
python create_dataset.py
```

This will create `data/dataset.json` with:
- 2 examples per tool for single-tool scenarios
- 2 multi-tool examples
- 2 unknown intent examples
- 2 paraphrased examples

#### Custom Dataset Generation

For production datasets, customize the generation parameters:

```bash
python create_dataset.py \
  --single-tool-examples 50 \
  --multi-tool-examples 100 \
  --unknown-intent-examples 30 \
  --adversarial-examples 20 \
  --paraphrase-count 200 \
  --dataset-name "dataset_v2.json"
```

#### Parameters

- `--single-tool-examples`: Number of examples per individual tool (default: 50)
- `--multi-tool-examples`: Number of multi-function scenarios (default: 50)
- `--unknown-intent-examples`: Number of unsupported query examples (default: 30)
- `--adversarial-examples`: Number of edge case examples (default: 5)
- `--paraphrase-count`: Number of paraphrased variations (default: 10)
- `--dataset-name`: Output filename (default: "dataset.json")

### Dataset Validation

Validate your generated dataset for quality and format compliance:

```bash
python validate_dataset.py data/dataset.json
```

This will:
- ✅ Check format compliance (ShareGPT format)
- 🔄 Remove duplicates and contamination
- 🧪 Test function execution (first 10 examples)
- 💾 Save cleaned dataset as `*_cleaned.json`

### Available Tools

The dataset generation includes examples for these function categories:

- **System Control**: `lock_screen`, `get_battery_status`, `set_volume`
- **Web Search**: `search_google`
- **Productivity**: `create_note`

Add new tools by editing `src/dataset/tools_description.py`.

### Dataset Upload (Optional)

Upload your dataset to Hugging Face Hub for sharing:

```bash
python upload_hf_dataset.py \
  --dataset-path data/dataset_cleaned.json \
  --repo-id "your-username/your-dataset-name"
```

### Dataset Structure

Generated datasets follow the ShareGPT format:

```json
[
  {
    "id": 1,
    "query": "Activate screen lock",
    "answers": [
      {
        "name": "lock_screen",
        "arguments": {}
      }
    ],
    "tools": [
      {
        "name": "lock_screen",
        "description": "Locks the laptop screen.",
        "parameters": {}
      }
    ]
  }
]
```

### Troubleshooting

**Common Issues:**

1. **Ollama Connection Error**: Ensure Ollama is running on `http://localhost:11434`
2. **Model Not Found**: Pull the required model with `ollama pull llama3.1:8b`
3. **Low Quality Output**: Try using a larger model like `llama3.1:8b` instead of smaller variants
4. **Memory Issues**: Reduce batch sizes in `settings.py` or use a smaller model

## Available Functions

### File Operations
* `copy_file`, `move_file`, `delete_file`, `create_folder`

### System Control
* `open_application`, `close_application`, `take_screenshot`, `lock_screen`, `get_battery_status`, `set_volume`

### Web & Media
* `open_url`, `search_google`, `play_music`, `pause_music`

### Productivity
* `create_note`

## Project Structure

```
custom-siri/
├── src/
│   ├── streamlit_siri_demo/   # Streamlit web demo
│   ├── functions/             # Function implementations
│   ├── dataset/               # Dataset generation tools
│   └── models/               # Trained model files
├── experiments/              # Experiment scripts
├── Dockerfile                # For using docker containers
├── notebook/                # Training notebooks
├── pyproject.toml          # Project configuration
└── README.md
```

## Development

### Key Dependencies
* **torch** (2.7+) - Deep learning framework
* **faster-whisper** - Speech-to-text processing
* **llama-cpp-python** - Local LLM inference
* **streamlit** - Web interface
* **sounddevice** - Audio recording
* **unsloth** - Efficient model fine-tuning

### Model Training Pipeline

The complete training pipeline is available in the Jupyter notebook and includes:

1. **Dataset Preparation**: Using custome Siri function-calling dataset
2. **Model Fine-tuning**: LoRA adaptation of Llama 3.1 8B
3. **Quantization**: GGUF format for efficient inference
4. **Evaluation**: 100% accuracy validation

### Adding New Functions

1. Implement functions in `functions.py`
2. Add schema to `functions` list
3. Register in `available_function_calls` dictionary

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**All courses, along with the generated date and fine-tuned model locations.**
* [Part 1: Build your own Siri. Locally. On-Device. No Cloud.](https://thehyperplane.substack.com/p/data-preparation-for-function-tooling)  
* [Part 2: Data Preparation for Function Tooling is boring ](https://thehyperplane.substack.com/p/data-preparation-for-function-tooling)
* [Part 3: Fine tune your own Siri](https://thehyperplane.substack.com/p/fine-tune-your-own-siri?r=5l0jbv)
* [Part 4: Deploy your Siri clone offline, on your phone](https://thehyperplane.substack.com/p/build-your-own-siri-locally-on-device)
* [Part 5: Bonus course](https://thehyperplane.substack.com/p/build-your-own-siri-locally-on-device)
* [Custom Datasets](https://huggingface.co/datasets/valex95/)
* [Fine-tuned Models](https://huggingface.co/CosminMihai02/)