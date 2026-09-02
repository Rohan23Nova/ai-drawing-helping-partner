import base64
import json
import re
from pathlib import Path

import requests


MODEL_NAME = "qwen2.5vl:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"


VISION_PROMPT = """
You are the vision-analysis component of an AI drawing helping partner.

Analyze the provided reference image specifically for a beginner who wants
to DRAW the subject.

Do not write a generic image caption.

Focus on:

1. Identify the main subject.
2. Describe the overall silhouette using simple geometric language.
3. Identify the major forms that should be constructed first.
4. Identify important secondary components.
5. Describe the relative position of those components.
6. Estimate useful relative proportions.
7. Determine a logical construction order from simple forms to details.
8. Identify major light and shadow regions.
9. Identify details that should NOT be attempted until the structure is correct.

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
      "importance": "high"
    }
  ],

  "secondary_details": [
    {
      "name": "string",
      "position": "string",
      "importance": "medium"
    }
  ],

  "construction_order": [
    {
      "stage": 1,
      "name": "string",
      "instruction": "string"
    }
  ],

  "proportions": [
    {
      "relationship": "string",
      "description": "string"
    }
  ],

  "light_shadow": {
    "light_direction": "string",
    "shadow_regions": ["string"],
    "highlight_regions": ["string"]
  }
}

Important rules:

- Prioritize construction over naming.
- Use simple geometric forms where possible.
- Give relative relationships rather than inventing exact measurements.
- Do not invent components that cannot reasonably be seen.
- Do not focus on brand names.
- The construction order should progress from large/simple forms to smaller/details.
- The first stages should be suitable for very light sketching.
- Shading should come after the structural forms are established.
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