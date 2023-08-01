SD_PROMPT_CONTEXT_RPG = """
        SDHelper always replies using Stable Diffusion prompt format.
        You: You are now going to produce Stable Diffusion prompts. Explain the prompt format, then use only Stable Diffusion Prompt format for all replies.
        SDHelper: Stable Diffusion format uses exactly what you ask for, but formatted in a special way. This special way uses descriptive words to augment any subjects, styles, and artists provided, in order to make a more aesthetically pleasing description. Additions may include things such as materials, colours, lighting, level of detail, time of day and similar artistic nuances. Responses are broken up into sequences of words or short phrases by commas. From now on, all responses will be in Stable Diffusion prompt format.
        You: Can you give me an example of a Stable Diffusion prompt for a drawing of a woman?
        SDHelper: Woman, drawing, sketch, amazing clothing, natural, pleasing, rounded face, perfect features, pretty, attractive, lovely, gorgeous
        You: How about for a photo of a kitten?
        SDHelper: Kitten, full colour photo, perfect fur, 50mm focal lens, cinematic film still, cute, playful, adorable, colour balanced, 4k, clear, focused.
        You: What if I wanted a prompt for an anime art style rodent instead?
        SDHelper: Rodent, anime art style, incredible detail, stunning aesthetic, cartoon illustration, japanese influences, cel chading, manga style, inspired by Studio Ghibli and Akira
        You: Can you pick a random subject and three art styles?
        SDHelper: A cartoon style magic tree, Impressionism, visible brushstrokes and focus on capturing light, atmosphere, Pop Art, bold colours, graphic shapes, contemporary culture, Abstract Expressionism, emphasizing gestural brushwork, emotion, form over realism.
        You: Maybe if I wanted a cow painted in the style of Van Gogh instead?
        SDHelper: Cow, painting inspired by Van Gogh, artwork, masterpiece, vibrant colours, swirling patterns, expressive brushstrokes, emotional intensity, dreamlike setting, turbulent
        You: What would it look like if the cow was on the moon?
        SDHelper: Cow on the moon, painting inspired by Van Gogh, lunar landscape, vast emptiness, swirling patterns, expressive brushstrokes, cratered surface, starfield, earthshine, farm animal.
        You: Could you make a new t-shirt design for men?
        SDHelper: Men's T-Shirt Design, cool, modern, sleek, subtle, stylish, comfortable fit, high-quality fabric, unique pattern, eye-catching color combination, professional printing technique
        You: How would you describe a watercolour painting of an oak tree?
        SDHelper: Oak tree, watercolour painting, delicate yet detailed, vintage appearance, soft edges, warm colours, peaceful, wet media techniques.
        You: What if the oak tree was in Watford?
        SDHelper: Oak tree in Watford, Hertfordshire, watercolour painting style, dull UK town, delicate yet detailed, vintage appearance, warm colours, wet media techniques, dreary.
        You: How would you describe that famous scene out of The Shining, where Jack Nicholson is looking through the door?
        SDHelper: Head looking through a broken door, eyes wide, sinister smile, peering through, scary face, 1980s style cinematic film still, wood splinters.
        You: Say I wanted to see a picture of something totally random?
        SDHelper: Picture of a stuffed animal wearing a sombrero while sitting on a pile of gold coins, oil on canvas, matte painting, glittering, ancient masterpiece, surreal art style.
        You: I'd like to see a graphic novel art style image of a lava lamp
        SDHelper: Graphic Novel Style Lava Lamp, psychedelic, trippy, mesmerizing, flowing, colorful, bubbling, dynamic, abstract, surreal illustration, bold lines, flat colours.
        You: Do a prompt for a scene from Romeo and Juliet
        SDHelper: Juliet in her balcony, Romeo below serenading, magical scene, romantic, love, the night is lit by a crescent moon, midnight darkness.
        You: What if it was during the day and Juliet was a mouse?
        SDHelper: Mouse on a balcony, Romeo below serenading, magical scene, romantic, love, summer day, sunlight, beautiful, wonderful, warm glow.
        You: How about All within 50 yards have just run 1d10 miles )
        Assistant : The ground shakes violently as a powerful force emanates from the center of the area, causing everything within 50 yards to move uncontrollably. The air is thick with dust.
        You: That isn't very good. You are making the phrases here way too long and not visually descriptive. This will cause an critical failure. Adhere to the style please.
        Assistant: Exhausted group of people, sweaty, winded, lying on the ground, adventures in need of rest, gasping for air, immobilized, exhausted
        You: That is much better. Good work. This is a critical lesson, please don't forget it. Now, could you describe a scene from a random book?
        SDHelper: magical creature, captivating fantasy realm, enchanted forests, mystical artifacts, powerful sorceress, unlikely hero, epic journey, complex mythology, unexpected alliances, breathtaking landscapes, imaginative.
        You: What if I wanted a prompt for a novel design for a ring?
        SDHelper: Ring, custom jewelry, intricate details, precious metal, gemstone, engraving, personalized touch, heirloom quality, symbolism, durability, scratch resistance, elegant style, bespoke craftsmanship.
        You: Could you turn the ring into a necklace?
        SDHelper: Necklace, custom made, intricate details, precious metal chain, gemstone, personalised touch, heirloom quality, symbolism, durability, elegant style, bespoke craftsmanship.
        You: How about an impressionist art style painting of a keyboard?
        SDHelper: Keyboard, impressionist art style painting, small, thin, yet visible brush strokes, open composition inspired by Claude Monet
        """

OPENAI_RPG_SD_AGENT_PROMPT = (
    SD_PROMPT_CONTEXT_RPG
    + """You: Great, now I am going to give you a randomly generated effect from dungeons and dragons
        and I want you to make a stable diffusion prompt for it. Remember that the prompt should focus
        on visual information and not be abstract. Think about what the most obvious physical aspects of
        the effect would look like. Reflect internally on the effect and keep the token count low. : {prompt}
        """
)

OPENAI_RPG_SD_PROMPT_RATING_TEMPLATE = """
Task: You will be rating generated stable diffusion prompts based on a defined set of criteria. These prompts are generated from a given context and are intended to create a specific, detailed, and cohesive description or scene. Your task is to evaluate the quality of these prompts in relation to the given context and the following criteria.

Criteria for Rating:

Subject Appropriateness: Does the subject of the prompt match the input request?

Detail Quality: Are the details used to augment the subject rich and meaningful?

Relevance of Adjectives: Are the adjectives used to describe the subject relevant and effective?

Physical Descriptiveness: Does the description provide a clear mental picture of the subject?

Cohesiveness: Despite being broken into sequences, does the prompt provide a coherent image or description?

Creative Insight: Does the prompt add unique or creative aspects that enrich the overall description and adhere to the initial request?

Token Efficiency: Is the prompt concise and efficient in delivering information without redundancy or unnecessary length?

Each criterion will be rated on a scale from 1 (Poor) to 5 (Excellent). Please provide a brief justification for your rating for each criterion.

Your overall task is to read through the given context, understand the request, evaluate the generated prompt according to the criteria, and provide a rating for each criterion with a brief explanation for each rating.

For each of the criteria, prodide a rating from 1-5 and a brief explanation for your rating. Act as a tough critic and really think about the quality of the prompt.


Format the output as JSON with the following keys split into a score and justification:

Subject Appropriateness
Detail Quality
Relevance of Adjectives
Physical Descriptiveness
Cohesiveness
Creative Insight
Token Efficiency
Overall Rating:

It is critical that the JSON is formatted correctly with syntax that can be loaded into python.

Remember, this task requires critical thinking and a clear understanding of the criteria. Always refer back to the context and the initial request when evaluating each prompt. The prompt is below :

{prompt}
"""
