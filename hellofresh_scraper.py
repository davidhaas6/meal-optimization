import requests

headers = {
    'authority': 'www.hellofresh.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJibG9ja2VkIjpmYWxzZSwiY291bnRyeSI6InVzIiwiZW1haWwiOiJmb290YmFsbGlzbXlsaWZlNzEyNEBnbWFpbC5jb20iLCJleHAiOjE2MzUyODI0OTksImlhdCI6MTYzNTI4MDY5OSwiaWQiOiI0MTZkODk2OS1mZGM4LTQ4YjMtYTlkOS1lNTkzNDNjM2E3ZWEiLCJpc3MiOiJjMWRjM2EzNS1iOWNmLTRjNjktOWUxMi1mZWQ2NzBiNmJiMGIiLCJqdGkiOiIzY2Y2MWM3MS0zMjY4LTQ1ZGUtYTYyMC00ODkwYjc2OTYzNzAiLCJtZXRhZGF0YSI6eyJuYW1lIjoiSm9zaHVhIE1vc2llciIsInBhc3N3b3JkbGVzcyI6ZmFsc2V9LCJyb2xlcyI6W10sInNjb3BlIjoiIiwic3ViIjoiNDE2ZDg5NjktZmRjOC00OGIzLWE5ZDktZTU5MzQzYzNhN2VhIiwidXNlcm5hbWUiOiJmb290YmFsbGlzbXlsaWZlNzEyNEBnbWFpbC5jb20ifQ.AhB9M3NkkEIXtWnSI1ivOqq1R857ZoYJuIgdCiiV30Q',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.hellofresh.com/my-account/deliveries/menu/2021-W42/9897612?recipePreviewId=6138d649ee4efd692531fc13',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cookie': '_HFtr=460402615.1619809851; _fbp=fb.1.1622658249746.304939361; hf_public_id=3770786b-b737-4658-b660-353ed2ddd204; _gcl_au=1.1.1884841636.1630070573; hfleadgen=1; G_ENABLED_IDPS=google; _gcl_aw=GCL.1630070721.CjwKCAjwmqKJBhAWEiwAMvGt6IRuyKMhopgjtE73xiAXyL4e0KPxIGvdPZPxsxq_I7ET5ON4od0deRoCNwAQAvD_BwE; hf_has_active_sub=1; hf_selected_plan=US-CBT6-4-2-0; hf_i=21905865; locale=en-US; hf_socialLogin=1; hf_has_freebies=0; __cf_bm=.Bgq1XzbnA8M4lwn2cXQcIZVgSp6HW9jHEGlwiTuwi4-1635280696-0-AWho0XSB+oLdTbrGcAOyIuvfjoNXumAPkbBpsTg9NKKAkaMZS7klTVdKmXhxlyTGEpT6mXS9W0DO7ZrWFl07mRNkQnK5p660kMd5wn7hdzMu; hf_cookie_permissions=,C0004,C0001,C0002,C0003,; apiV2Auth={%22access_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJibG9ja2VkIjpmYWxzZSwiY291bnRyeSI6InVzIiwiZW1haWwiOiJmb290YmFsbGlzbXlsaWZlNzEyNEBnbWFpbC5jb20iLCJleHAiOjE2MzUyODI0OTksImlhdCI6MTYzNTI4MDY5OSwiaWQiOiI0MTZkODk2OS1mZGM4LTQ4YjMtYTlkOS1lNTkzNDNjM2E3ZWEiLCJpc3MiOiJjMWRjM2EzNS1iOWNmLTRjNjktOWUxMi1mZWQ2NzBiNmJiMGIiLCJqdGkiOiIzY2Y2MWM3MS0zMjY4LTQ1ZGUtYTYyMC00ODkwYjc2OTYzNzAiLCJtZXRhZGF0YSI6eyJuYW1lIjoiSm9zaHVhIE1vc2llciIsInBhc3N3b3JkbGVzcyI6ZmFsc2V9LCJyb2xlcyI6W10sInNjb3BlIjoiIiwic3ViIjoiNDE2ZDg5NjktZmRjOC00OGIzLWE5ZDktZTU5MzQzYzNhN2VhIiwidXNlcm5hbWUiOiJmb290YmFsbGlzbXlsaWZlNzEyNEBnbWFpbC5jb20ifQ.AhB9M3NkkEIXtWnSI1ivOqq1R857ZoYJuIgdCiiV30Q%22%2C%22token_type%22:%22Bearer%22%2C%22expires_in%22:1800%2C%22refresh_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NDA0NjQ2OTksImlhdCI6MTYzNTI4MDY5OSwiaXNzIjoiYzFkYzNhMzUtYjljZi00YzY5LTllMTItZmVkNjcwYjZiYjBiIiwianRpIjoiNWRiN2VjODEtNTRiYy00NmI5LTk0ZDctY2NlMDY3NzY3YWQ4Iiwic3ViIjoiNDE2ZDg5NjktZmRjOC00OGIzLWE5ZDktZTU5MzQzYzNhN2VhIn0.HUrgeYzXBvfz7lxWI_gQTZAqEoyDYA0hL85iTN3wgpk%22%2C%22expire_with_session%22:false}; _safari_api_poll=true; _HFtr_gid=450286411.1635280699; __cfruid=0eaa06d5c9e5f833458b708b820f6051ab1e418b-1635280701; _HFtr_gat=1',
}

params = (
    ('recipeId', '6138d649ee4efd692531fc13'),
    ('country', 'us'),
    ('locale', 'en-US'),
)

response = requests.get('https://www.hellofresh.com/gw/recipes/recipes/6138d649ee4efd692531fc13', headers=headers, params=params)
print(response.json()['nutrition'])