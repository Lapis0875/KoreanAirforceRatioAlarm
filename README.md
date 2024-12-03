# KoreanAirforceRatioAlarm

공군 지원현황 정보를 원하는 시간대에 자동으로 조회해 웹훅으로 보내줍니다.
모든 보라매 여러분들의 입대 준비 및 군생활을 응원합니다.
+ 저는 현재 공군 병 856기로 복무중입니다 ㅎㅎ

# How To Use?

## 1. Setup

이 저장소를 포크(fork)해주세요. 이후, 자신의 디스코드 서버에 적당한 채널을 만들어 웹훅을 하나 만들어주세요.
이후, 저장소의 설정에 들어가 Settings > Secrets and Variables > Actions > Repository Secrets 항목에 "WEBHOOK_DISCORD_URL" 이라는 이름으로 새로운 Secret을 만들고, 그 값으로 앞서 만든 웹훅의 URL을 저장해주세요.

## 2. Configuration

이제, 어떤 군대(육해공) 의 지원 현황을 볼 것인지 정해야 합니다.
`config.json` 파일을 열면 아래와 같이 구성되어 있습니다.

```json5
{
    "webhook": {
        "username": "{웹훅_유저_이름}",
        "avatar": "{웹훅_유저_프로필_이미지_url}"
    },
    "query": {
        "start_date": "{모집_시작_일자}",       // YYYY.MM.DD 형식
        "finish_date": "{모집_종료_일자}",      // YYYY.MM.DD 형식
        "category": {  // 검색할 지원현황의 모집구분
            "name": "{모집구분_이름}",    // 모집구분 텍스트
            "index": {모집구분_번호}      // 선택 창에서 이 모집구분이 몇 번째인가? (제일 위를 0번이라 했을 때) 를 정수로.
        },
        "recruit": "{입영년월}",            // YYYY년MM월 형식
        "apply": {     // 지운 시점의 정보
            "year": {지원연도},         // YYYY 형식의 정수
            "month": {지원월}           // MM 형식의 정수
        }
    }
}
```

위 파일을 자신의 상황에 맞게 수정 후 포크(fork)한 자신의 저장소에 커밋(commit) 해주세요.

## 3. Wait
조금 기다리면, 웹훅을 설정한 디스코드 채널로 군 지원 현황에 대한 메세지가 전송됩니다.
기본적으로, 2시간마다 전송하도록 설정해 두었으나 변경하고 싶을 경우 `.github/workflows/discord_webhook_action.yml` 파일을 수정해주세요.
관련 사항에 대한 문의는 이슈로 해주시면 답변드리겠습니다.
또, 아직 Github Action을 종료하는 방법이 따로 없습니다.
군 지원 기간이 끝나 더이상 알람을 받고 싶지 않은 경우 `.github/workflows/discord_webhook_action.yml`의 schedule 항목을 통으로 지워 알람이 오지 않게 할 수 있습니다.
