from typing import TypedDict, cast
from json import load

__all__ = ("WebhookConfig", "QueryConfig", "ActionConfig", "read_config")

class WebhookConfig(TypedDict):
    """Webhook 관련 설정 컨피그입니다."""
    url: str        # Discord Webhook URL
    username: str   # Discord Webhook Username
    avatar: str     # Discord Webhook Avatar URL

class FormSelection(TypedDict):
    """HTML Form에서 셀렉트 메뉴에서 선택한 값을 표현하는 형식입니다."""
    name: str           # 항목의 텍스트
    index: int          # 항목의 인덱스 (0번째부터 몇번째에 위치하는가.)

class YearAndMonth(TypedDict):
    """연도와 달 정보를 각각 받는 JSON 객체."""
    year: int
    month: int

class QueryConfig(TypedDict):
    """군 지원 현황을 조회하기 위해 검색에 필요한 정보들입니다."""
    start_date: str             # 지원 시작 일자. (YYYY.MM.DD 형식)
    finish_date: str            # 지원 시작 일자. (YYYY.MM.DD 형식)
    category: FormSelection     # 지원 분야. 현황 조회 시 '모집구분' 선택하는 항목의 내용과 일치해야 한다.
    recruit: str                # 입영 날짜 (YYYY년MM월 형식)
    apply: YearAndMonth         # 지원 기준 연도 및 달 정보. ex) 2023년 12월 지원

class ActionConfig(TypedDict):
    """Action 설정에 필요한 컨피그 데이터들을 읽어옵니다."""
    webhook: WebhookConfig
    query: QueryConfig

def read_config() -> ActionConfig:
    with open("./config.json", mode="rt", encoding="utf-8") as config_file:
        config: ActionConfig = cast(ActionConfig, load(config_file))
    return config
    