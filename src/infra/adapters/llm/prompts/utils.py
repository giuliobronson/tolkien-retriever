from pathlib import Path

from infra.adapters.utils import load_text

PROMPTS_DIR = Path(__file__).parent


def build_rules_agent_system_prompt(game_name: str) -> str:
    content = load_text(PROMPTS_DIR / "rules_agent_system.md")
    return content.replace("$game_name", game_name)
