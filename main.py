import asyncio
import json
import os
from datetime import datetime
import traceback
from smart_assertions import soft_assert

from next_gen_ui_langgraph.readme_example import search_movie, movies_agent, ngui_cfg, ngui_agent
from report_generator import setup_html_report, create_report_directory
from utils.logger import get_logger

logger = get_logger("next_gen_ui")

llm_model = "llama3.2"


def run():
    # Load test data
    with open("testdata/toy_story_dataset_5.json", 'r') as file:
        data = json.load(file)

    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(__file__)
    base_report_dir = os.path.join(base_dir, "AI_Reports")

    # Create report directory and setup HTML report
    run_dir = create_report_directory(base_report_dir, timestamp, llm_model)
    run_index_html = setup_html_report(base_report_dir, run_dir, timestamp)

    file_name = os.path.join(run_dir, f"temp_results_{timestamp}.json")
    for i in range(len(data)):
        user_prompt = data[i]['Prompt']
        expected_component = data[i].get('expected_component')
        try:
            logger.info("----------Starting LLM ------")
            logger.info(f"user inputs {user_prompt}")
            movie_response = movies_agent.invoke(
                {"messages": [{"role": "user", "content": user_prompt}]}
            )
            ngui_response = asyncio.run(
                ngui_agent.ainvoke(movie_response, ngui_cfg)
            )

            first_rendition = ngui_response["renditions"][0]
            content_json = json.loads(first_rendition.content)
            logger.info(f"content_json actual output from LLM {content_json}")
            status = content_json.get('component') == expected_component
            soft_assert(status, "Component are not matching")
            logger.info(f"status equals{status}")
            logger.info(f"Actual UI component w.r.t user input {content_json.get('component')}")
            logger.info("----------End LLM ------")

            test_data = {
                "user_prompt": user_prompt,
                "expected_component": expected_component,
                "actual_results": content_json.get('component'),
                "status": status,
                "llm_model": llm_model,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error during processing prompt index {i}: {e}", exc_info=True)
            test_data = {
                "user_prompt": user_prompt,
                "expected_component": expected_component,
                "actual_results": None,
                "status": False,
                "llm_model": llm_model,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "exception_type": e.__class__.__name__,
                "traceback": traceback.format_exc()
            }
        finally:
            results.append(test_data)
            with open(file_name, 'w') as file_system:
                json.dump(results, file_system, indent=2)

    # Log summary
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("status") is True)
    failed_tests = total_tests - passed_tests
    logger.info("=" * 60)
    logger.info(f"TEST SUMMARY")
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Passed: {passed_tests}")
    logger.info(f"Failed: {failed_tests}")
    logger.info(f"Pass Rate: {(passed_tests / total_tests * 100):.2f}%")
    logger.info(f"Results saved to: {file_name}")
    if run_index_html:
        logger.info(f"HTML Report: {run_index_html}")
    else:
        logger.info("HTML Report: Not generated (template setup failed)")
    logger.info("=" * 60)

    return results


if __name__ == '__main__':
    run()
