from loguru import logger


def replace_prompt(prompt: str, replacement_map: dict) -> str:
    logger.info(prompt)
    for key in replacement_map.keys():
        if "{" + key + "}" not in prompt:
            logger.info(key)
            raise KeyError(f"Invalid key '{key}' in replacement_map")
    return prompt.format(**replacement_map)
