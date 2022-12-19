from urllib.request import Request, urlopen

url = 'https://api-tokyochallenge.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=LbXulxOlPDNiWPexUX62e0xDg9buLZQP00HmhQNU3k4'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
request = Request(url, headers)

response_body = urlopen(request).read()
print(response_body)