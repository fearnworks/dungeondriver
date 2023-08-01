from dungeon_driver.prompts.prompt_builder import replace_prompt
import pytest


def test_should_replace_multiple_map_values():
    prompt = "The {animal} jumped over the {object}."
    replacement_map = {"animal": "cat", "object": "fence"}

    new_prompt = replace_prompt(prompt, replacement_map)

    assert new_prompt == "The cat jumped over the fence."


def test_replace_prompt_with_invalid_key():
    prompt = "The {animal} jumped over the {object}."
    replacement_map = {"animal": "cat", "object": "fence", "color": "red"}

    with pytest.raises(KeyError, match="Invalid key 'color' in replacement_map"):
        replace_prompt(prompt, replacement_map)
