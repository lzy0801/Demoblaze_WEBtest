from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
import time
import random

# 初始化 Edge 浏览器
service = EdgeService()
driver = webdriver.Edge()
driver.maximize_window()

# 设置 WebDriverWait 的超时时间
wait = WebDriverWait(driver, 20)

# 生成随机用户名
username = f"testuser{random.randint(1000, 9999)}"
password = "testpass123"


try:
    # ==================== 1. 打开首页 ====================
    print("1. 打开首页")
    driver.get("https://www.demoblaze.com/")
    time.sleep(2)

    # ==================== 2. 注册功能 ====================
    print("2. 开始注册...")
    signup_button = driver.find_element(By.ID, "signin2")
    signup_button.click()
    wait.until(EC.visibility_of_element_located((By.ID, "sign-username")))

    username_field = driver.find_element(By.ID, "sign-username")
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "sign-password")
    password_field.send_keys(password)

    register_button = driver.find_element(By.XPATH, "//button[text()='Sign up']")
    register_button.click()
    driver.save_screenshot("screenshot_1_login_success.png")  # 截图
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        print("注册弹窗：", alert.text)
        print("注册成功！")
        driver.save_screenshot("screenshot_3_signup_success.png")  # 截图
        alert.accept()
    except:
        print("无注册弹窗")
        print("注册失败！")
    time.sleep(2)

    # ==================== 3. 登录功能 ====================
    print("3. 开始登录...")
    login_button = driver.find_element(By.ID, "login2")
    login_button.click()
    wait.until(EC.visibility_of_element_located((By.ID, "loginusername")))

    loginusername_field = driver.find_element(By.ID, "loginusername")
    loginusername_field.send_keys(username)

    loginpassword_field = driver.find_element(By.ID, "loginpassword")
    loginpassword_field.send_keys(password)

    login_submit_button = driver.find_element(By.XPATH, "//button[text()='Log in']")
    login_submit_button.click()
    print("登录成功！")
    driver.save_screenshot("screenshot_5_login_success.png")  # 截图
    time.sleep(3)

    # ==================== 4. 浏览商品功能 ====================
    print("4. 浏览商品...")
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "card-title")))
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    if products:
        print(f"找到{len(products)}个商品，点击第一个商品：{products[0].text}")
        products[0].click()
    else:
        print("未找到商品")
    print("商品浏览成功！")
    time.sleep(2)
    driver.save_screenshot("screenshot_6_product_detail.png")  # 截图

    # ==================== 5. 商品加入购物车功能 ====================
    print("5. 加入购物车...")
    add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']")))
    add_btn.click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        print("加入购物车弹窗：", alert.text)
        print("加入购物车成功！")
        driver.save_screenshot("screenshot_8_add_to_cart_success.png")  # 截图
        alert.accept()
    except:
        print("无加入购物车弹窗")
    time.sleep(2)

    # ==================== 6. 进入购物车页面 ====================
    print("6. 进入购物车...")
    cart_icon = driver.find_element(By.ID, "cartur")
    cart_icon.click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success")))
    driver.save_screenshot("screenshot_9_cart_page.png")  # 截图
    time.sleep(2)

    # ==================== 7. 删除购物车商品 ====================
    print("7. 删除购物车商品...")
    delete_btns = driver.find_elements(By.XPATH, "//a[text()='Delete']")
    if delete_btns:
        delete_btns[0].click()
        print("已点击删除按钮")
        time.sleep(2)
    else:
        print("购物车无商品可删")
    time.sleep(2)

    # ==================== 8. 浏览商品分类并添加到购物车 ====================
    print("8. 浏览Laptops商品分类并添加到购物车")
    driver.find_element(By.ID, "nava").click()
    time.sleep(2)
    try:
        # 使用 XPath 定位 Laptops 分类链接
        laptops_category_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@onclick=\"byCat('notebook')\"]"))
        )
        laptops_category_link.click()  # 点击Laptops链接
        time.sleep(2)
        driver.save_screenshot("screenshot_13_laptops_category.png")  # 截图

        # 获取商品列表
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "card-title")))
        products = driver.find_elements(By.CLASS_NAME, "card-title")

        if products:
            # 点击第一个商品
            products[0].click()
            time.sleep(2)
            driver.save_screenshot("screenshot_14_laptops_product_detail.png")  # 截图

            # 加入购物车
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']")))
            add_btn.click()
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.accept()
                print("成功从Laptops分类添加商品到购物车！")

            except:
                print("该Laptops分类下没有加入购物车按钮")
                driver.save_screenshot("screenshot_15_laptops_add_to_cart_failure.png")  # 截图
            time.sleep(2)
        else:
            print("该分类下没有商品")
    except Exception as e:
        print(f"浏览Laptops商品分类并添加到购物车失败: {e}")

    # ==================== 9. 结算功能 ====================
    print("9. 测试订单结算功能...")
    # 重新添加一个商品
    driver.find_element(By.ID, "nava").click()
    time.sleep(2)
    products = driver.find_elements(By.CLASS_NAME, "card-title")
    if products:
        products[0].click()
        time.sleep(2)
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']")))
        add_btn.click()
        time.sleep(2)
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        time.sleep(2)
        cart_icon = driver.find_element(By.ID, "cartur")
        cart_icon.click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success")))
        driver.save_screenshot("screenshot_2_login_success.png")  # 截图
        time.sleep(2)
        # 点击Place Order
        place_order_button = driver.find_element(By.XPATH, "//button[text()='Place Order']")
        place_order_button.click()
        wait.until(EC.visibility_of_element_located((By.ID, "orderModalLabel")))

        name_field = driver.find_element(By.ID, "name")
        name_field.send_keys("测试用户")

        country_field = driver.find_element(By.ID, "country")
        country_field.send_keys("中国")

        city_field = driver.find_element(By.ID, "city")
        city_field.send_keys("广州")

        card_field = driver.find_element(By.ID, "card")
        card_field.send_keys("1234567890123456")

        month_field = driver.find_element(By.ID, "month")
        month_field.send_keys("12")

        year_field = driver.find_element(By.ID, "year")
        year_field.send_keys("2025")
        time.sleep(2)
        driver.save_screenshot("screenshot_3_login_success.png")  # 截图

        purchase_button = driver.find_element(By.XPATH, "//button[text()='Purchase']")
        purchase_button.click()
        time.sleep(2)
        print("订单结算完成！")
        driver.save_screenshot("screenshot_18_order_confirmation.png")  # 截图
    else:
        print("无商品可结算")


except Exception as e:
    print(f"发生错误：{str(e)}")
finally:
    print("关闭浏览器...")
    driver.quit()