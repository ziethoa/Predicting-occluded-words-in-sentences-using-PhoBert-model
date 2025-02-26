from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Cấu hình trình duyệt
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Hàm để click "Xem thêm sản phẩm" và thu thập dữ liệu
def scrape_products(category_url, load_more_xpath):
    driver.get(category_url)
    products = []

    while True:
        try:
            # Đợi nút "Xem thêm sản phẩm" xuất hiện
            load_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, load_more_xpath))
            )
            # Click nút
            ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()
            time.sleep(2)  # Đợi nội dung tải
        except:
            print("Đã tải hết sản phẩm.")
            break

    # Lấy toàn bộ sản phẩm
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Tìm khu vực chứa sản phẩm
    product_section = soup.find('div', class_="px-4 pt-3 md:px-0 md:pt-0")

    if product_section:
        product_items = product_section.find_all('div')

        for product in product_items:
            try:
                name = product.find('h3').text.strip()
                link = product.find('a')['href']
                products.append({
                    'Name': name,
                    'Link': f"https://nhathuoclongchau.com.vn{link}"
                })
                print(f"Đã lấy dữ liệu sản phẩm: {name}")
            except AttributeError:
                continue
    else:
        print("Không tìm thấy phần tử ")

    return products

# URL nhóm trị liệu (ví dụ)
category_url = "https://nhathuoclongchau.com.vn/thuoc/thuoc-te-boi"
load_more_xpath = "/html/body/div[1]/div[1]/div[2]/div[3]/div/div[4]/div/section/div[2]/button/span"

# Gọi hàm và lấy dữ liệu
all_products = scrape_products(category_url, load_more_xpath)

# Xử lý dữ liệu trùng lặp
df = pd.DataFrame(all_products)
df = df.drop_duplicates(subset=['Name', 'Link'], keep='first')  # Giữ mục đầu tiên

# Lưu dữ liệu vào file CSV
df.to_csv("boi.csv", index=False, encoding='utf-8-sig')
print("Done!")
# Đóng trình duyệt
driver.quit()
