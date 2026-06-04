import os
import re
import json
import urllib.request

GITHUB_USERNAME = "Sandeepkumar13M"
README_PATH = "README.md"
START_MARKER = "<!-- PROJECTS-START -->"
END_MARKER = "<!-- PROJECTS-END -->"

EMOJI_MAP = {
    "JavaScript": "\u{1F7E1}",
    "Python": "\u{1F40D}",
    "Java": "\u2615",
    "TypeScript": "\u{1F535}",
    "HTML": "\u{1F310}",
    "CSS": "\u{1F3A8}",
    "Shell": "\u{1F4BB}",
}


def get_repos():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=100&type=public"
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    with urllib.request.urlopen(req) as resp:
        repos = json.loads(resp.read().decode())
    # Exclude the profile repo itself
    return [r for r in repos if r["name"] != GITHUB_USERNAME and not r["fork"]]


def build_projects_block(repos):
    lines = []
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        desc = repo.get("description") or "No description provided."
        lang = repo.get("language") or "Code"
        stars = repo.get("stargazers_count", 0)
        emoji = EMOJI_MAP.get(lang, "\u{1F4E6}")
        stars_badge = f"\u2B50 {stars}" if stars > 0 else ""
        lines.append(f"### {emoji} [{name}]({url})")
        lines.append(f"> {desc}")
        lines.append(f"")
        lang_str = f"**Tech:** {lang}"
        if stars_badge:
            lang_str += f" &nbsp; {stars_badge}"
        lines.append(lang_str)
        lines.append(f"")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def update_readme(new_block):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL
    )
    replacement = f"{START_MARKER}\n{new_block}{END_MARKER}"
    new_content = pattern.sub(replacement, content)

    if new_content == content:
        print("No changes detected.")
        return False

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"README updated with {len(repos)} projects.")
    return True


if __name__ == "__main__":
    repos = get_repos()
    block = build_projects_block(repos)
    update_readme(block)
