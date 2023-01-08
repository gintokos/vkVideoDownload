import time
import undetected_chromedriver as uc

def get_cookies(profile_dir:str)->str:
    driver = uc.Chrome(user_data_dir=profile_dir)
    driver.get('https://vk.com/')
    
    vk_cookies = list()
    
    while "https://vk.com/feed" not in driver.current_url:
        time.sleep(5)
    
    vk_cookies = list()
    cookies = driver.get_cookies()
    for cookie in cookies :
        vk_cookies.append(f'{cookie["name"]}={cookie["value"]}')
    
    driver.close()
    
    str_cookies = "; ".join(vk_cookies)
    
    with open("cookies.txt","w") as f:
        f.write(str_cookies)
    
    return str_cookies
