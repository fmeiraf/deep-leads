from typing import Callable

from deepeval import evaluate
from deepeval.metrics import GEval  # type: ignore
from deepeval.test_case import LLMTestCase, LLMTestCaseParams  # type: ignore
from rich import print as rprint

from src.evals.utils.lead_comparison import display_leads_comparison
from src.types import EvalParams


async def test_correctness_with_visual_comparison(
    call_agent: Callable,
    eval_params: EvalParams,
    researcher_model: str = "openai:gpt-4.1-mini-2025-04-14",
    orchestrator_model: str = "openai:gpt-4.1-mini-2025-04-14",
    n_results_search: int = 5,
) -> dict[str, GEval | float]:
    """Enhanced test function with visual lead comparison before evaluation"""
    correctness_metric = GEval(
        name="Correctness",
        model="gpt-4.1-mini",
        criteria="Determine if the 'actual output' contains all the information from the 'expected output'.",
        evaluation_steps=[
            "Check if all the leads on 'actual output' are present in 'expected output'",
            "Check the quality of the leads on 'actual output' compared to 'expected output'",
            "Heavily penalize leads on 'actual output' that are not present in 'expected output'",
        ],
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        threshold=0.5,
    )

    result, query = await call_agent(
        eval_params.query_params,
        researcher_model=researcher_model,
        orchestrator_model=orchestrator_model,
        n_results_search=n_results_search,
    )

    print("=" * 80)
    rprint(f"Query \n{query}")
    print("=" * 80)

    # Visual comparison before evaluation
    print("\n" + "=" * 80)
    print("VISUAL LEAD COMPARISON")
    print("=" * 80)
    recall_matches, total_extra = display_leads_comparison(
        result.leads, eval_params.expected_results.leads
    )

    # evaluation
    test_case = LLMTestCase(
        input=query,
        actual_output=result.to_string(),
        expected_output=eval_params.expected_results.to_string(),
    )

    eval_results = evaluate(test_cases=[test_case], metrics=[correctness_metric])

    return {
        "eval_results": eval_results,
        "recall_matches": recall_matches,
        "total_extra_leads": total_extra,
    }
