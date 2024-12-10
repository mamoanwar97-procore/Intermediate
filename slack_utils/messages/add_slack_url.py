from .utils import is_singular, construct_prs_list, construct_message, thank_you

list_emoji = ":slack:"


def construct_header(prs: list[str]):
    repo = "is a repo" if is_singular(prs) else "are some repos"
    verb_to_have = "has its" if is_singular(prs) else "have their"
    header = f"Hello Team, There {repo} that {verb_to_have} slack url missing"
    return header


def construct_footer(prs: list[str]):
    identifier = "it" if is_singular(prs) else "them"
    footer = (
        f"Can you add the slack url for {identifier} when you get a chance?{thank_you}"
    )
    return footer


def add_slack_url_message(repos: list[str]):
    message = construct_message(
        [
            construct_header(repos),
            construct_prs_list(repos, list_emoji),
            construct_footer(repos),
        ]
    )
    return message
