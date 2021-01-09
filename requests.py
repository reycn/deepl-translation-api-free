import time
import random
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def deepl_translator(sentence:str, lang_src:str='auto', lang_tgt:str='ZH')-> str:

    proxies={
        'https': 'socks5://127.0.0.1:1080'
    }
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [
        OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value
    ]

    user_agent_rotator = UserAgent(software_names=software_names,
                                   operating_systems=operating_systems,
                                   limit=100)

    user_agent = user_agent_rotator.get_random_user_agent()
    sentence = '"' + sentence + '"'
    u_sentence = sentence.encode("unicode_escape").decode()
    data = '{"jsonrpc":"2.0","method": "LMT_handle_jobs","params":{"jobs":[{"kind":"default","raw_en_sentence":' + u_sentence + ',"raw_en_context_before":[],"raw_en_context_after":[],"preferred_num_beams":4,"quality":"fast"}],"lang":{"user_preferred_langs":["EN","ZH"],"source_lang_user_selected":"EN","target_lang":"ZH"},"priority":-1,"commonJobParams":{},"timestamp":' + str(
            int(time.time() * 10000)) + '},"id":' + str(
                random.randint(1, 100000000)) + '}'

    session = requests.Session()
    # session.proxies.update(proxies)
    try:
        r = session.post(
            'https://www2.deepl.com/jsonrpc',
            headers={
                'content-type':
                'application/json',
                # 'user-agent': user_agent,
                "user-agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "origin":
                "https://www.deepl.com",
                "accept":
                "*/*",
                "sec-fetch-mode":
                "cors",
                "sec-fetch-dest":
                "empty",
                "sec-fetch-site":
                "same-site",
                "dnt":
                "1",
                "referer":
                "https://www.deepl.com/",
                "accept-language":
                "zh-Hans-CN,zh-CN;q=0.9,zh;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5",
            },
            data=data.encode(),
            proxies=proxies)
    except requests.exceptions.ConnectionError as c:
        print(f'Connection failed:\n{str(c)}')

    if r.json():
        try:
            result = r.json()['result']['translations']
            print(result)
            if len(result) > 1:
                return ' '.join(i['postprocessed_sentence']
                                for i in result[0]['beams'][0])
            else:
                return result[0]['beams'][0]['postprocessed_sentence']
        except:
            try:
                return(r.json()['error']['message'])
            except:
                return('Unknown error!')
    else:
        print("Responce.json() not found!")

# time.sleep(2)
print(
    deepl_translator('''Translation works correctly'''))
