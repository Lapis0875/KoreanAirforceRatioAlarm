from typing import Final, Literal, Optional, TypedDict
from dataclasses import dataclass, field
from sys import version_info

__all__ = ("KoreaAirforceJobDataResponse", "JSON", "MilitaryRatioResponse", "MWPT_MMA_Response", "KoreaAirforceJobData", "parse_job_response")

class KoreaAirforceJobDataResponse(TypedDict):
    """공군 지원현황 데이터의 응답 내에서, 직종별 항목에 해당하는 JSON 데이터."""
    gsteukgi_nm: str        # 접수특기_이름 (직종 이름)
    gsteukgi_cd: str        # 접수특기_코드 (직종 코드)
    
    seonbal_pcnt: str       # 선발_퍼센트 (모집(선발)계획인원)
    jeopsu_pcnt: str        # 접수_퍼센트 (접수인원)
    rate: str               # 비율 (경쟁률)
    extremes: str           # 초과 (과부족)

if version_info >= (3, 12):
    type JSON = dict[str, KoreaAirforceJobDataResponse | list | dict | str | int | None]
else:
    JSON = dict[str, KoreaAirforceJobDataResponse | list | dict | str | int | None]

class MilitaryRatioResponse(TypedDict):
    """병무청 군 입대 접수현황 응답에 대한 부분적인 타입 표현."""
    jwsjsHyeonHwangMWVOList: list[KoreaAirforceJobDataResponse]

class MWPT_MMA_Response(TypedDict):
    """병무청 쿼리 응답 JSON의 포맷."""
    vo: JSON            # 뭔지 모르겠는데 잔뜩 옴. JSON 포맷.
    mjSearch: Optional[dict[Literal["jwsjsHyeonHwangMWVOList"], list[KoreaAirforceJobDataResponse]] | JSON]    # 마찬가지로 뭐 많이오는데 이 안에 
    result: str

@dataclass(frozen=True)
class KoreaAirforceJobData:
    """공군 지원현황 직종별 데이터"""
    job_name: Final[str] = field(compare=True)   # 직종 이름
    job_code: Final[int] = field(compare=True)   # 직종 코드
    
    planned: Final[int] = field(compare=True)    # 모집(선발)계획인원
    enrolled: Final[int] = field(compare=True)   # 접수인원
    rate: Final[float] = field(compare=False)    # 경쟁률
    more_or_less: Final[int] = field(compare=False) # 과부족

    @property
    def is_below(self) -> bool:
        """이 직종이 현재 선발인원보다 미달 상태인지 판단한다.
        
        Returns:
            bool: 미달일 경우 True, 아닐 경우 False.
        """
        return self.more_or_less < 0

def parse_job_response(resp: KoreaAirforceJobDataResponse) -> KoreaAirforceJobData:
    """API 응답으로 받은 군 지원 현황 JSON을 대응하는 KoreaAirforceJobData 객체로 파싱한다.

    Args:
        resp (KoreaAirforceJobDataResponse): 응답으로 받은 JSON 데이터.

    Returns:
        KoreaAirforceJobData: 파싱된 객체.
    """
    
    return KoreaAirforceJobData(
        job_name=resp["gsteukgi_nm"],
        job_code=int(resp["gsteukgi_cd"]),
        planned=int(resp["seonbal_pcnt"]),
        enrolled=int(resp["jeopsu_pcnt"]),
        rate=float(resp["rate"]),
        more_or_less=int(resp["extremes"])
    )
    
