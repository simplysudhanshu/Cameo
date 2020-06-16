from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import sys
import time
import colors


# class drive:
#     def __init__(self):
#         self.content = ""
#         self.options = Options()
#         self.options.add_argument('--headless')
#         self.options.add_argument('--disable-gpu')
#
#         self.driver = webdriver.Chrome(options=self.options)
#
#         self.driver.get("https://rentry.co/cameo-room/raw")
#         print("page opened")
#
#     def refresh(self):
#         print("in refresh")
#         while True:
#             start_time = time.time()
#             time.sleep(20)
#             text_element = self.driver.find_element_by_xpath('html/body/pre').text
#             print(text_element)
#             # print(f'time : {time.time() - start_time}')
#             self.content = text_element
#
#             self.driver.refresh()
#
#
# def delete_last_line():
#     "Use this function to delete the last line in the STDOUT"
#
#     # cursor up one line
#     sys.stdout.write('\x1b[1A')
#
#     # delete last line
#     sys.stdout.write('\x1b[2K')


# new_drive = drive()
#
# options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--disable-gpu')
#
# driver = webdriver.Chrome(options=options)
#
# driver.get("https://rentry.co/cameo-room/edit")
#


# def everything_else():
#     # for i in range(5):
#     #     print(i)
#     #     time.sleep(1)
#     #     num, word = new_drive.content.split(',')
#     #     print(num, word)
#
#     time.sleep(1)
#     body = driver.find_element_by_xpath('//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]/pre/span')
#     body.send_keys(Keys.LEFT_CONTROL + 'a')
#     body.send_keys(Keys.DELETE)
#
#     time.sleep(2)
#     new_body = driver.find_element_by_xpath('//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]/pre/span')
#     new_body.send_keys('NEW DATA')
#
#     edit_code = driver.find_element_by_xpath('//*[@id="id_edit_code"]')
#     edit_code.send_keys("cameo_room")
#
#     save = driver.find_element_by_xpath('//*[@id="submitButton"]')
#     save.click()
#     print("done")
#
#
# else_thread = threading.Thread(target=everything_else)
# refresh = threading.Thread(target=new_drive.refresh)
#
#
# refresh.start()
# else_thread.start()
#

#
# rules = "\nSome RULES before we get into it :\n--\n" \
#         "1.  Don't rush into anything in life. Join the game ONE PLAYER AT A TIME.\n\n" \
#         "2.  Be patient in life. You will have to WAIT for the room to be initialised and connected.\n" \
#         "    (It depends on your internet connection and fragility of my code, but mostly your internet. MEH.\n\n" \
#         "3.  It's the spirit of sportsmanship that drives the world. Don't be an asshole. DON'T CHEAT.\n\n" \
#         "4.  Lower the expectations, lesser the hurt. This game might have some BUGS and ERRORS, we'll keep making it better.\n" \
#         "--------------------------------------------------------------------------------------------------------------------"
#
# print(rules)
#
# a = 'abcdef'
# b = 'abc'
# c = []
# for index in range(max(len(a), len(b))):
#     try:
#         if a[index] == b[index]:
#             continue
#         else:
#             c.append()


# def trial(s: str, what: str):
#     to_print = ''
#
#     if "looked" in what and "swap" in what:
#         to_print += f'{colors.UNDERLINE}{colors.red}{s}{colors.ENDC} '
#
#     elif "swap" in what:
#         to_print += f'{colors.red}{s}{colors.ENDC} '
#
#     elif "looked" in what:
#         to_print += f'{colors.UNDERLINE}{s}{colors.ENDC} '
#
#     print(to_print)
#
#
# trial('s', 'swapped')
a = ['simply', 'prince of persia']
max_length = len(max(a, key=len))

for item in a:
    print(f"{item:>{max_length}} : 1")