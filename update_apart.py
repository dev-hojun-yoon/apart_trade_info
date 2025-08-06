import requests
import os
import ssl
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter

# class TLS13Adapter(HTTPAdapter):
#     def init_poolmanager(self, *args, **kwargs):
#         kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1_1
#         return super().init_poolmanager(*args, **kwargs)



load_dotenv()

SERVICE_KEY = os.getenv('SERVICE_KEY')
print(SERVICE_KEY)
str_year = str(datetime.today().year)
month = datetime.today().month
str_month = f'{month:02d}'
CURRENT_YM = str_year + str_month
README_PATH = "README.md"

URL = f'http://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade?serviceKey={SERVICE_KEY}&LAWD_CD=11680&DEAL_YMD={CURRENT_YM}&pageNo=1&numOfRows=10'

# session = requests.Session()
# session.mount('https://', TLS13Adapter())

def get_data():
    """국토교통부 아파트 실거래가 api 를 통해 강남 압구정동 매일 10개 데이터를 가져옵니다."""
    response = requests.get(URL)
    print(response)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        raise Exception(f"API 요청 실패: {response.status_code}")

    root = ET.fromstring(response.text)
    print(root)

    headers = ["법정동", "단지명", "전용면적", "계약일", "거래금액(만원)", "층", "건축연도", "거래유형", "등기일자"]
    md_table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]

    for item in root.findall('.//item'):
        umdNm = item.findtext("umdNm", "").strip()
        aptNm = item.findtext("aptNm", "").strip()
        excluUseAr = item.findtext("excluUseAr", "").strip()
        dealDay = item.findtext("dealDay", "").strip()
        dealAmount = item.findtext("dealAmount", "").strip()
        floor = item.findtext("floor", "").strip()
        buildYear = item.findtext("buildYear", "").strip()
        dealingGbn = item.findtext("dealingGbn", "").strip()
        rgstDate = item.findtext("rgstDate", "").strip()

        md_table.append(
            f"| {umdNm} | {aptNm} | {excluUseAr} | {dealDay} | {dealAmount} | {floor} | {buildYear} | {dealingGbn} | {rgstDate} |"
        )

    return '\n'.join(md_table)

def update_readme():
    """README.md 파일을 업데이트"""
    apart_info = get_data()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# 🚩 강남 압구정동 실거래가 확인 (국토교통부 실거래가 API)

이 리포지토리는 국토교통부 실거래가 API 를 활용하여 강남 압구정동 실거래가 10개 데이터 를 업데이트합니다.

<br>
<br>

## 실거래 정보
{apart_info}

<br>
<br>

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
    """

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme_content)


if __name__ == '__main__':
    update_readme()
