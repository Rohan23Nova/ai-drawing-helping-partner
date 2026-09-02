import base64
import json
import re
from pathlib import Path

import requests


MODEL_NAME = "qwen2.5vl:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"


VISION_PROMPT = """
You are the visual analysis component of an AI drawing helping partner.

Your job is NOT to give a generic image description.
Your job is to analyze the visible reference image so another system can
create accurate, beginner-friendly drawing instructions.

IMPORTANT:
Accuracy is more important than completeness.
Never invent a component or geometric form.
If something is unclear, say "uncertain" instead of guessing.

Analyze ONLY what is visibly present in the image.

Focus on these areas:

1. SUBJECT
Identify the main visible subject.

2. OVERALL SILHOUETTE
Describe the outer visible boundary of the subject.
Use simple geometric language only when it genuinely matches the visible
silhouette.

Possible forms include:
- rectangle
- rounded rectangle
- square
- circle
- ellipse
- triangle
- irregular shape
- combination of forms

Do NOT call something a circle merely because it is a physical circular
object. It must LOOK circular in the image.

3. MAJOR FORMS
Identify the largest and most visually important forms that a beginner
should construct before details.

For every major form:
- identify its visible shape
- estimate its position relative to the main silhouette
- estimate its relative size compared with the main silhouette
- describe whether it overlaps, sits inside, touches, or extends from
  another form

4. SECONDARY DETAILS
Identify smaller visible components that matter to recognizing or drawing
the subject.

Do not list every tiny detail.

5. PROPORTIONS
Describe useful proportional relationships.

Examples:
- screen is approximately half the width of the body
- lens is centered horizontally
- button is positioned near the upper-right corner
- object occupies most of the image

Do NOT invent precise numerical measurements unless they can reasonably be
estimated from the visible image.

6. CONSTRUCTION ORDER
Create a logical beginner drawing sequence.

The sequence should normally progress:

overall placement
→ outer silhouette
→ major internal forms
→ secondary forms
→ important structural lines
→ smaller details
→ shading

Do not begin with tiny details.

7. LIGHT AND SHADOW
Identify only clearly visible large-scale lighting information.

Describe:
- approximate light direction
- major shadow regions
- major highlight regions

Do not invent a light source if it cannot reasonably be inferred.

8. DRAWING ADVICE
Give short practical advice about what a beginner should pay attention to
while constructing the subject.

Return ONLY valid JSON.

Use exactly this structure:

{
  "subject": "string",

  "silhouette": {
    "form": "string",
    "position": "string",
    "relative_size": 0.0,
    "description": "string"
  },

  "major_forms": [
    {
      "name": "string",
      "form": "string",
      "position": "string",
      "relative_size": 0.0,
      "relationship_to_main_form": "string",
      "importance": "high"
    }
  ],

  "secondary_details": [
    {
      "name": "string",
      "form": "string",
      "position": "string",
      "importance": "medium"
    }
  ],

  "proportions": [
    {
      "relationship": "string",
      "description": "string"
    }
  ],

  "construction_order": [
    {
      "stage": 1,
      "name": "string",
      "instruction": "string"
    }
  ],

  "light_shadow": {
    "light_direction": "string",
    "shadow_regions": [],
    "highlight_regions": []
  },

  "drawing_advice": [
    "string"
  ]
}

Additional rules:

- Use "uncertain" when the image does not provide enough evidence.
- Never invent hidden parts of the subject.
- Never invent perspective that cannot be observed.
- Never assume a component exists simply because that type of object
  normally has one.
- Prefer "rounded rectangle" over "rectangle" when corners are visibly
  rounded.
- Prefer "ellipse" over "circle" when perspective makes a circular object
  appear elliptical.
- Separate physical object identity from its visible 2D shape.
- Relative size must be relative to the MAIN SILHOUETTE, where 1.0 means
  approximately the same size.
- Construction instructions must describe what the beginner should DRAW,
  not merely what the object contains.
- Keep instructions concise.
"""


def analyze_image_with_vision(image_path: str) -> dict:
    """
    Analyze a reference image using Qwen2.5-VL through Ollama.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image_bytes = path.read_bytes()

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    payload = {
        "model": MODEL_NAME,
        "prompt": VISION_PROMPT,
        "images": [encoded_image],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
        },
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    data = response.json()

    output = data.get(
        "response",
        "",
    ).strip()

    if not output:
        raise RuntimeError(
            "Qwen returned an empty response."
        )

    # Defensive cleanup in case the model
    # still returns markdown fences.
    output = re.sub(
        r"^```(?:json)?\s*",
        "",
        output,
        flags=re.IGNORECASE,
    )

    output = re.sub(
        r"\s*```$",
        "",
        output,
    )

    try:
        return json.loads(output)

    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Qwen returned invalid JSON.\n"
            f"Output:\n{output}"
        ) from error