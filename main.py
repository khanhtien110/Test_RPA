from Configuration.config import Config
from robocorp.tasks import task
from robocorp import browser
from Modules import *
import time
import os
import shutil
from RPA.Desktop import Desktop
import random
from openpyxl import load_workbook
import asyncio
import json
import threading


@task
def main():
    try:

        env = "development"
        # env = "production"

        config = Config(env)

        rpa_tracker = RPATracker(config)
        rpa_tracker.write_message("khanhtien", False)
        rpa_tracker.start_tracking("Robot function")

        # # Login
        # rpa_tracker.start_tracking("Login")
        # browser = RoboBrowser(config.data, rpa_tracker)
        # is_login = browser.handle_login()
        # if is_login == False:
        #     raise Exception("Failed to login")

        # is_logout = browser.handle_logout()
        # browser.cleanup_browser()
        # rpa_tracker.end_tracking(False)
        # # Login

        # # Re-login
        # rpa_tracker.start_tracking("Relogin")
        # rpa_tracker.debug("OK")
        # rpa_tracker.track("Click Back button")
        # browser.robo_browser.click_element('//*[@id="content"]/div/div/p[2]/a')

        # rpa_tracker.track("Input username")
        # browser.robo_browser.input_text(
        #     browser.data["username_selector"], browser.data["id"]
        # )

        # rpa_tracker.track("Input password")
        # browser.robo_browser.input_text(
        #     browser.data["password_selector"], browser.data["pw"]
        # )

        # rpa_tracker.track("Click Login button")
        # browser.robo_browser.click_button(browser.data["btnLogin_selector"])
        # browser.handle_logout()
        # rpa_tracker.end_tracking(False)
        # # Re-login

        # rpa_tracker.start_tracking("Send Email")
        # imap_smtp = ImapSMTP(config.data, rpa_tracker)
        # imap_smtp.send_message(
        #     recipients=config.get_value("recipients"),
        #     subject="RPA test message",
        #     body="<strong>TPDV</strong><br><br><br><strong>THL ONE</strong>",
        #     cc="khanhtien.nguyen@thlone.vn",
        #     bcc="vinh.tran@thlone.vn",
        #     attachments="attachments\\attachment1.txt,attachments\\attachment2.txt",
        # )

        # rpa_tracker.end_tracking(False)

        temp_data = [random.randint(1, 100) for _ in range(10)]
        array_2d = [[random.randint(1, 100) for _ in range(100)] for _ in range(100)]
        data = [
            {"Tháng": "Tháng 1", "Sản phẩm": "A", "Doanh thu": 100},
            {"Tháng": "Tháng 1", "Sản phẩm": "B", "Doanh thu": 200},
            {"Tháng": "Tháng 2", "Sản phẩm": "A", "Doanh thu": 150},
            {"Tháng": "Tháng 2", "Sản phẩm": "B", "Doanh thu": 250}
        ]

        rpa_excel = RPAExcel(config.data, rpa_tracker)
        rpa_excel.open_excel("templates\\template1.xlsx")
        # Điền dữ liệu vào sheet
        # rpa_excel.fill_data(data, sheet_name="Sheet1", start_row=0, start_col=0)
        # Chèn công thức vào cột
        # rpa_excel.insert_formula("Sheet1", list_column=["A"], formula_type="sum", direction="vertical")
        # # Tạo bảng Pivot
        # rpa_excel.create_pivot("Sheet1", data, pivot_index=["Tháng"], pivot_columns=["Sản phẩm"], pivot_values=["Doanh thu"])
        # # Chèn hình ảnh vào ô
        rpa_excel.insert_image(".images\\image.png", cell="A1", sheet_name="Sheet1")
        # # Tạo biểu đồ
        # rpa_excel.create_chart("Sheet1", chart_type="bar", data_range=[1, 1, 3, 4], position="E5")
        
        # temp_data = [random.randint(1, 100) for _ in range(10)]
        # array_2d = [[random.randint(1, 100) for _ in range(100)] for _ in range(100)]

        # rpa_excel = RPAExcel(config.data, rpa_tracker)
        # rpa_excel.open_excel("templates\\template1.xlsx")
        # rpa_excel.fill_data(temp_data)

        # rpa_excel.save_wb()

        # rpa_excel.cleanup()

        _client = RPAWebSocket(config_data=config.data, rpa_tracker=rpa_tracker)
        loop = asyncio.get_event_loop()
         
        while True:
            loop.run_until_complete(_client.connect_to_socket_server())
            # loop.run_until_complete(_client.send_message(json.dump("\"message\":\"Hello Hello Hello\"")))
        
        loop.create_task(_client.receive_message())
        
        time.sleep(5)
        loop.run_until_complete(_client.close())

    except Exception as e:
        pass

async def connect(client):
    while True:
        await client.connect_to_socket_server()