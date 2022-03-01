import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer': 'https://google.com.br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,en;q=0.9',
        'Pragma': 'no-cache',
    }

#browser settings
options = Options()
options.add_argument("--allow-running-insecure-content")
options.add_argument("no-sandbox");
#options.add_argument("headless"); 
options.add_argument("start-maximized");
options.add_argument("window-size=1900,1080");
options.add_argument("no-sandbox")
options.add_argument("--no-sandbox");
options.add_argument("--ignore-certificate-errors");
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
options.add_argument('referer=https://google.com.br')

capabilities = {
'browserName': 'chrome',
'chromeOptions':  {
   'useAutomationExtension': False,
   'forceDevToolsScreenshot': True,
   'args': ['--start-maximized', '--disable-infobars']
 }
} 

class selDriver:
  def __init__(self):
      self.driver = webdriver.Chrome(executable_path="modules\driver\chromedriver.exe", options=options)
      
