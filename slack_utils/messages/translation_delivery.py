from slack_utils.messages.utils import is_singular, construct_prs_list, construct_message, thank_you

list_emoji = ":translate2:"
translation_delivery = "Translation Delivery"


def construct_header(prs: list[str]):
    translation_delivery_pr = (
        f"a {translation_delivery} PR"
        if is_singular(prs)
        else f"some {translation_delivery} PRs"
    )
    header = f"Hello Team, We have just dropped {translation_delivery_pr}"
    return header


def construct_footer(prs: list[str]):
    identifier = "it" if is_singular(prs) else "them"
    footer = (
        f"Can you give {identifier} a quick review when you get a chance?{thank_you}"
    )
    return footer


def translation_delivery_message(repos: list[str]):
    message = construct_message(
        [
            construct_header(repos),
            construct_prs_list(repos, list_emoji),
            construct_footer(repos),
        ]
    )
    return message
