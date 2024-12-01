from fastapi import Header


def get_language(x_wanted_language: str = Header(default="ko")) -> str:
    return x_wanted_language
