# Deep Lead Generator 🎯

An intelligent AI-powered lead generation system that uses LLM agents to systematically research and extract high-quality professional contacts based on specific search criteria.

The Deep Lead Generator is designed to automate the time-intensive process of finding and qualifying leads for business development, research collaboration, or networking purposes. It uses a sophisticated AI agent that can:

- **Systematically search** the web for professionals matching specific criteria
- **Extract structured contact information** from various sources (university directories, research institutions, professional profiles)
- **Validate and score** [NOT IMPLEMENTED YET] lead quality against predefined standards
- **Provide comprehensive evaluations** with visual comparisons and metrics

## Key Features

#### 🎯 **Smart Research Parameters**

The system breaks down lead research into structured components:

- **WHO**: Target roles/professions (e.g., "professors", "researchers", "directors")
- **WHAT**: Field/industry specialization (e.g., "Human Nutrition", "AI", "Cancer Research")
- **WHERE**: Geographic or institutional constraints (e.g., "Edmonton", "universities")
- **CONTEXT**: Additional qualifiers (e.g., "lab leaders", "published authors")

#### 🔧 **Multi-Phase Research Process**

1. **Discovery Phase**: Broad web searches to identify relevant institutions and sources
2. **Site Mapping**: Systematic exploration of promising websites to find directory structures
3. **Deep Extraction**: Targeted extraction of detailed contact information from specific pages
4. **Quality Validation**: Verification and scoring of extracted leads [NOT IMPLEMENTED YET]

#### 📊 **Evaluation System**

- Human-verified test datasets for benchmarking
- Visual lead comparison with detailed field-by-field analysis
- Automated scoring using LLM-based evaluation metrics
- Recall and precision tracking for continuous improvement

## 📁 Project Structure

```
deep_leads/
├── src/
│   ├── types.py                    # Core data models and type definitions
│   ├── agents/                     # Agent implementations (extensible)
│   └── evals/                      # Evaluation framework
│       ├── human_verified_searches.py  # Test datasets with verified leads
│       └── lead_comparison.py      # Visual comparison and analysis tools
├── notebooks/
│   ├── agent_test_1.ipynb        # Main agent implementation and testing
│   └── eval_scrapping.ipynb      # Scraping evaluation and analysis
├── pyproject.toml                # Project configuration and dependencies
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- OpenAI API key
- Tavily API key (for web research)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd deep_leads
   ```

2. **Install dependencies using UV**:

   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env.local` file with:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

### Usage

#### Basic Lead Research

```python
from src.types import ResearchParams

# Define your research parameters
params = ResearchParams(
    who_query="professors",
    what_query="Human Nutrition",
    where_query="University of Alberta",
    context_query="leading research labs"
)

# Run the agent (see notebooks for full implementation)
results = await deep_leads_agent.run(build_final_query(params))
```

#### Running Evaluations

The system includes comprehensive evaluation capabilities:

```python
# Run evaluation with visual comparison
await test_correctness_with_visual_comparison(EDMONTON_HUMAN_NUTRITION_RESEARCH_UNIT)
```

## 🔍 Current Capabilities

### ✅ What Works Well

- Systematic multi-phase research approach
- Rich evaluation framework with visual feedback
- Extensible architecture for different lead types

### 🚧 Known Limitations

- May hallucinate contact information when details are sparse
- Search paths can be narrow and susceptible to page retrieval errors
- Limited parallel exploration of alternative research paths
- Needs stronger fact-checking to prevent filter drift during expanded searches
- Could benefit from more websearch options to enable for varied exploration

## 🛣️ Roadmap

- [ ] Improve lead_comparison using embeds of semantic checks (now relying on string match which is not optimal)
- [ ] Add evals on important lead data individually
- [ ] Enhanced fact-checking and validation pipeline
- [ ] Broader search path exploration with fallback strategies
- [ ] Real-time lead scoring and prioritization

---

_Built with ❤️ for intelligent lead generation and research automation_
