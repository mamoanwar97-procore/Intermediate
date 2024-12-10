def is_singular(prs: list[str]):
    return len(prs) == 1


def construct_prs_list(prs: list[str], list_emoji: str = ""):
    prs_with_trucks = [list_emoji + " " + item for item in prs]
    concatenated_prs = "\n".join(prs_with_trucks)
    return concatenated_prs


def construct_message(parts: list[str]):
    message = "\n\n".join(parts)
    return message


thank_you = "Thank you :globe_with_meridians:"
