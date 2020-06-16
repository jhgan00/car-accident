import requests
import json
import fire
from tqdm import tqdm
from getpass import getpass


# noinspection PyAttributeOutsideInit
class TaasCrawler:
    def __init__(self):
        self.login_url = 'https://taas.koroad.or.kr/web/umt/lmt/initLogin.do'
        self.data_url = 'http://taas.koroad.or.kr/gis/srh/ash/selectAccidentInfo.do'
        self.headers = {
            'Host': 'taas.koroad.or.kr',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.payload = {
            "searchType": "00",
            "pageIndex": "1",
            "zoneYn": "false",
            "engnCode": "00",
            "startAcdntYear": "2007",  # 검색 시작 연도
            "endAcdntYear": "2019",  # 검색 종료 연도
            "acdntGaeCode": "01,02,03,04",  # 사고조건: 사망, 중상, 경상, 부상신고
            "acdntCode": "110,120,130,140,199"  # 사고유형: 차대사람(횡단중, 차도통행중, 길가장자리구역통행중, 보도통행중, 기타)
        }

        self.LOGIN_INFO = {}

    def set_login_info(self):
        ID = input("ID: ")
        # noinspection PyPep8Naming
        PWD = getpass("Password: ")
        self.LOGIN_INFO = {
            'loginid': str(ID),
            'loginpwd': str(PWD)
        }

    def set_payload(self, condition):
        self.payload["searchSimpleCondition"] = condition

    def request_and_parse(self):
        with requests.Session() as s:
            login_res = s.post(self.login_url, data=self.LOGIN_INFO)
            if login_res.status_code != 200:
                raise Exception(f"Login Failed: Returns {login_res.status_code}")
            print(f"로그인 성공: {self.LOGIN_INFO['loginid']}")
            print(f"데이터 수집을 시작합니다")
            result = []
            code = ['11%', '26%', '27%', '28%', '29%', '30%', '31%', '36%', '41%', '42%', '43%', '44%', '45%', '46%',
                    '47%', '48%', '50%']
            sido = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남',
                    '제주']
            legaldong_dict = dict(zip(code, sido))

            for code in tqdm(code):
                self.payload['legaldongCode'] = code
                res = s.post(self.data_url, data=json.dumps(self.payload), headers=self.headers)
                if res.status_code != 200:
                    raise Exception(
                        f"""
                        요청 실패 \n
                        시도코드: {sido} \n
                        {res.status_code} \n
                        {res.text}
                        """
                    )
                json_obj = res.json()['resultValue']['accidentInfoList']
                tqdm.write(f"{legaldong_dict[code]} 지역: {len(json_obj)}건")
                result += json_obj
        print(f"총 {len(result)} 건의 데이터를 수집하였습니다. \n")
        return result

    def run(self, kids=True):
        print("TAAS 로그인")
        self.set_login_info()
        if kids:
            for condition in ["27", "29"]:
                self.set_payload(condition)
                json_obj = self.request_and_parse()
                filepath = f"data/kids-accident-{condition}.json"
                print(f"데이터 저장 중: {filepath}")
                with open(filepath, "w") as f:
                    json.dump(json_obj, f)
                print("저장되었습니다.")
        else:
            json_obj = self.request_and_parse()
            filepath = f"data/accident-total.json"
            print(f"데이터 저장 중: {filepath}")
            with open(filepath, "w") as f:
                json.dump(json_obj, f)
            print("저장되었습니다.")


if __name__ == '__main__':
    fire.Fire(TaasCrawler)
