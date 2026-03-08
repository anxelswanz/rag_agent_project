from project.utils.config_handler import prompts_conf
from project.utils.log_handler import logger
from project.utils.path_tool import get_abs_path


def load_system_prompt():
    try:
        system_prompt_path = get_abs_path(prompts_conf['main_prompt_path'])
    except KeyError as e:
        logger.error('Could not find system prompt path')
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error('Could not find system prompt file')
        raise e


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error('rag_summarize_prompt_path not found')
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error('resolve RAG prompt failed')
        raise e

def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf['report_prompt_path'])
    except KeyError as e:
        logger.error('Could not find report_prompt_path prompt path')
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error('resolve report prompt failed')
        raise e

if __name__ == '__main__':
    print(load_system_prompt())