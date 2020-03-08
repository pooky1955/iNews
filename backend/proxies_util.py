# optional code if you want to add proxies when fetching

import requests
from bs4 import BeautifulSoup
def get_proxies():
  url = 'https://free-proxy-list.net'
  response = requests.get(url,verify=False)
  soup = BeautifulSoup(response.text)
  proxies_table = soup.select("table#proxylisttable>tbody")[0]
  all_ips = []
  for row in proxies_table.find_all("tr"):
    all_columns = row.find_all("td")
    ip,port,_,_,proxy_type,_,https_enabled,_ = [tag.text for tag in all_columns]
    if https_enabled == "yes" and proxy_type == "elite proxy":
      complete_ip = f"{ip}:{port}"
      all_ips.append(complete_ip)
if __name__ == "__main__":
  all_proxies = get_proxies()
