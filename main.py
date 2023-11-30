from typing import Any
from requests import post
from json import dump
from discord_webhook_utils import Color, Embed, Field, WebhookMessage

from config import WebhookConfig, QueryConfig, ActionConfig, read_config
from models import KoreaAirforceJobDataResponse, KoreaAirforceJobData, MWPT_MMA_Response, parse_job_response

config: ActionConfig = read_config()

def build_params() -> dict[str, Any]:
    """요청 파라미터를 구성한다."""
    query_cfg: QueryConfig = config["query"]
    recruit_str = query_cfg["recruit"]

    return {
        "grjjeopsok_yn": "N",
        "gun_gbcd": 3,
        "iyyj_ym": recruit_str,
        "iyyjsijak_ym": f"{recruit_str[0:4]}{recruit_str[-3:-1]}",  # 연도 및 월만 잘라내기.
        "jeopsu_jrdtm": query_cfg["finish_date"],
        "jeopsu_sjdtm": query_cfg["start_date"],
        "mjiljeong_no": "13823",
        "mjjwgyegeup_cd": "001",
        "mojip_gbcd": query_cfg["category"]["index"],
        "mojip_gbcdm": query_cfg["category"]["name"],
        "mojip_tms": query_cfg["apply"]["month"],
        "mojip_yy": query_cfg["apply"]["year"],
        "authpage": "SSGJiWonHH_L",
        "jeongryeolss": 1
    }

def send_data(data: list[KoreaAirforceJobDataResponse]):
    """요청을 처리한 내용을 웹훅으로 전송하기 위해 파일로 가공한다."""
    webhook_cfg = config["webhook"]
    msg = WebhookMessage(
        content="군 지원 정보를 조회했습니다!",
        avatar_url=webhook_cfg["avatar"],
        username=webhook_cfg["avatar"],
        embeds=[]
    )
    
    for resp in data:
        do: KoreaAirforceJobData = parse_job_response(resp)
        msg.embeds.append(Embed(
            title=f"{do.job_name} ({do.job_code})",
            fields=[
                Field("모집 인원", str(do.planned), False),
                Field("경쟁률", str(do.rate), True),
                Field("접수 인원", str(do.enrolled), False),
                Field("과부족", f"{do.more_or_less} ({'미달' if do.is_below else '초과'})", True)
            ],
            color=Color.Green
        ))
    
    with open("./response.json", mode="wt", encoding="utf-8") as res_file:
        dump(msg.to_dict(), res_file, ensure_ascii=False, indent=4)

def handle_400():
    """400번대, 즉 잘못된 요청에 대한 처리."""
    webhook_cfg = config["webhook"]
    msg = WebhookMessage(
        content="잘못된 API 요청입니다! 프로젝트 저장소에 이슈를 통해 제보해주세요!",
        avatar_url=webhook_cfg["avatar"],
        username=webhook_cfg["avatar"],
    )
    with open("./response.json", mode="wt", encoding="utf-8") as res_file:
        dump(msg.to_dict(), res_file, ensure_ascii=False, indent=4)

def handle_500():
    """500번대, 즉 서버 문제에 대한 처리."""
    webhook_cfg = config["webhook"]
    msg = WebhookMessage(
        content="병무청 API 서버에 문제가 있습니다! 프로그램의 문제가 아니며 병무청 서버가 정상화 되는걸 기다려 주세요!",
        avatar_url=webhook_cfg["avatar"],
        username=webhook_cfg["avatar"],
    )
    with open("./response.json", mode="wt", encoding="utf-8") as res_file:
        dump(msg.to_dict(), res_file, ensure_ascii=False, indent=4)

def handle_error():
    """의도치 않은 요청을 받았을 경우, 웹훅을 통해 오류를 알린다."""
    webhook_cfg = config["webhook"]
    msg = WebhookMessage(
        content="병무청에서 군 지원 현황 정보를 조회하던 중 오류가 발생했습니다!",
        avatar_url=webhook_cfg["avatar"],
        username=webhook_cfg["avatar"],
    )
    with open("./response.json", mode="wt", encoding="utf-8") as res_file:
        dump(msg.to_dict(), res_file, ensure_ascii=False, indent=4)

def main():
    resp = post(
        url="https://mwpt.mma.go.kr/caisBMHS/dmem/dmem/mwgr/gjwn/selectMBJWHyeonHwang_JH.json?hwamyeon_id=SSGJiWonHH_L",
        params=build_params(),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
    )
    
    match (resp.status_code // 100):
        case 4:
            handle_400()
            return
        case 5:
            handle_500()
            return
    
    json: MWPT_MMA_Response = resp.json()
    try:
        data: list[KoreaAirforceJobDataResponse] = json["mjSearch"]["jwsjsHyeonHwangMWVOList"]
        with open("./last_resp.json", mode="wt", encoding="utf-8") as last_resp_file:
            dump({"mjSearch/jwsjsHyeonHwangMWVOList": data}, last_resp_file, ensure_ascii=False, indent=4)
        send_data(data)
    except KeyError:
        handle_error()
    finally:
        print("Done!")

if __name__ == "__main__":
    main()
