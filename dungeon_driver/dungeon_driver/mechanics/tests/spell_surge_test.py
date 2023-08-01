from dungeon_driver.mechanics.spell_surge_generator import (
    SpellSurgeGenerator,
    ReplacementConfig,
)


def test_generate_subject_replacement():
    # Given
    prompt = "The caster casts a spell on the target."
    generator = SpellSurgeGenerator()

    replacement_config = ReplacementConfig(target="Orc Warrior", caster="Human Mage")
    # When
    output = generator.generate_subject_replacement(prompt, replacement_config)

    # Then
    assert output == "The Human Mage casts a spell on the Orc Warrior."


def test_roll_dice_in_string():
    # Given
    s = "The caster rolls 2d6 for damage."
    generator = SpellSurgeGenerator()

    # When
    output = generator.roll_dice_in_string(s)

    # Then
    assert "2d6" not in output
    assert isinstance(output, str)
