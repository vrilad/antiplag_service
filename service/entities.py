from typing_extensions import TypedDict

class CheckInput(TypedDict):

    name: str
    ref_text: str
    candidate_text: str


class CheckResult(TypedDict):

    percent: str