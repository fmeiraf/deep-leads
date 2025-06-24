# Deep Lead Generator

## Project Overview

I decided to build a **Lead Search** agent that uses LLM agents to systematically research and extract high-quality professional contacts based on specific search criteria.

Reasons why I picked this project:

- This was something I wanted for another project I am working on.
- I wanted something that had very simple and composable tools but that could scale chaining them properly (so the challenge of optimizing gets more interesting).
- I was particularly interested in testing this after reading the [latest Anthropic article on **multi agents**](https://www.anthropic.com/engineering/built-multi-agent-research-system).

## Technical Stack

- **Agent Framework**: PydanticAI for structured agent interactions
- **Web Research**: Tavily API for intelligent web search
- **LLM Models**: OpenAI GPT-4.1 series, Anthropic Claude series
- **Evaluation**: DeepEval for automated assessment
- **Visualization**: Rich library for terminal-based result presentation
- **Data Models**: Pydantic for type-safe data structures

## Architecture & Implementation

### Core Components

#### 1. **Structured Data Models** (`src/types.py`)

- **`ResearchParams`**: Defines search parameters using WHO/WHAT/WHERE/CONTEXT framework
- **`Lead`**: Comprehensive contact model with validation and string representation
- **`LeadResults`**: Container for multiple leads with aggregation methods
- **`EvalParams`**: Evaluation framework combining query parameters with expected results

```python
class ResearchParams(BaseModel):
    who_query: str    # Target roles/professions
    what_query: str   # Field/industry specialization
    where_query: Optional[str]  # Geographic/institutional constraints
    context_query: Optional[str]  # Additional qualifiers
```

#### 2. **Multi-Pattern Agent Architecture** (`src/agents/`)

**Single Agent Pattern** (`single_agent_pattern.py`):

- Comprehensive 252-line system prompt with detailed search methodology
- 3-phase research process: Discovery → Site Mapping → Extraction
- Built-in error handling and parallel tool execution
- Strict anti-hallucination constraints

**Multi-Agent Pattern** (`multi_agent_pattern.py`):

- Orchestrator-Researcher coordination system
- Strategic task decomposition and delegation
- Parallel execution across multiple specialized researchers
- Enhanced quality control through distributed verification

#### 3. **Web Research Tools**

Both agent patterns include:

- `browse_web()`: Tavily-powered web search with configurable result counts
- `get_website_map()`: Site structure analysis for systematic exploration
- `get_website_content()`: Targeted content extraction from specific URLs

## Evaluation System

### Human-Verified Test Dataset (`src/evals/human_verified_searches.py`)

- **716 lines** of meticulously curated test cases
- Two complexity levels: narrow-scope and broad-scope searches
- Real-world scenarios: University of Alberta faculty searches
- Ground truth data with complete contact information

### Visual Evaluation Framework (`src/evals/`)

**Automated Evaluation** (`eval_runner.py`):

- DeepEval integration with custom GEval metrics
- LLM-based correctness scoring
- Recall and precision tracking
- Visual lead comparison before evaluation

**Rich Visual Comparison** (`utils/lead_comparison.py`):

- Field-by-field lead comparison with color coding
- Match detection based on name/email similarity
- Missing/extra lead identification
- Comprehensive summary statistics with recall calculations

## Results & Performance Analysis

### Model Comparison Study

Systematic evaluation across multiple LLM models:

- **OpenAI**: GPT-4.1, GPT-4.1-mini, GPT-4.1-nano
- **Anthropic**: Claude Sonnet 4, Claude 3.7 Sonnet, Claude 3.5 Sonnet

### Evaluation Metrics

- **G-Eval Score**: LLM-based correctness assessment
- **Recall Rate**: Percentage of expected leads successfully found
- **Extra Leads**: Count of wrongly suggested leads

### Key Findings

For more context check the images shared!

#### ✅ **Strengths Demonstrated**

- Stronger models have an easier time using sub-agents for task assigment
- Parallel tool calling seems to be something used by a wide range of models and it reallys speeds up the inference time

#### 🚧 **Identified Limitations**

- Models allucinate a lot of information on the lack more details (example: sees a name on a article but can't find the person inforamtion, it then allucinate their contact info)
- The search paths are very narrow and and can totally get out of path when faced with some timeout or other types of page retrieval errors.
- Even though many parallel calls are made the explorations paths are still not enough to cover possibilities.
- There is an important need to have a fact check phase. The model tends to ignore important filtering cases like WHERE and CONTEXT clausese. This normally happens when models expand search and then the filters get "lost" in their context or attention

## Future Enhancements

### Planned Improvements

- **Enhanced Fact-Checking**: Stronger validation pipeline to prevent filter drift after first submission of leads
- **Broader Search Exploration**: Multiple parallel research paths with fallback strategies
- **Semantic Lead Comparison**: Embedding-based similarity instead of string matching
- **Real-time Lead Scoring**: Dynamic quality assessment and prioritization
- **Individual Field Evaluation**: Granular accuracy metrics for each contact field
