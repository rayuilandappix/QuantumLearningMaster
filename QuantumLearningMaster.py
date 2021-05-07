from inspect import isabstract
from tkinter.constants import FALSE
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
from selenium import webdriver
import time
import datetime
import os
from os import getcwd,sep
cwd = getcwd()
from selenium.webdriver.chrome.options import Options
import json
import PySimpleGUI as sg
import configparser

cf=configparser.ConfigParser()
cf.read("config.ini",encoding="utf-8-sig")
url=cf.get("ADDRESS","url")
checkurl=cf.get("ADDRESS","url2")

waittime=200
autop=False

print("================================\n量子学习大师3.00\n================================")
print("请不要关闭本窗口，在弹出的窗口中操作\n================================")

layout=[
    [sg.Text("可以在此处调整设置，并按启动按钮来开始学习")],
    [sg.Text("模式选择"),sg.Button("工作模式(默认)"),sg.Button("挂机模式")],
    [sg.Text("自动换P开关"),sg.Button("关闭"),sg.Button("打开(默认)")],
    [sg.Button("启动")]
]

window = sg.Window('学习助手设置', layout, no_titlebar=False, auto_size_buttons=False)
while True:
    event,value = window.Read()
    if(event=="工作模式(默认)"):
        print("已选择工作模式，此模式每200秒轮询一次")
        waittime=200
    if(event=="挂机模式"):
        waittime=60
        print("已选择挂机模式，此模式每60秒轮询一次")
    if(event=="关闭"):
        autop=True
        print("自动换P已关闭")
    if(event=="打开(默认)"):
        autop=False
        print("自动换P已打开")
    if(event=="启动"):
        break
    if(event==WIN_CLOSED):
        exit()

window.Close()


print("正在打开浏览器")
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(f'{cwd}{sep}chromedriver',chrome_options=options)

#driver.maximize_window()
driver.get(url)
print("请在弹出的浏览器窗口里登录")
time.sleep(5)

while(True):
    nowurl=driver.current_url
    if(nowurl==checkurl):
        print("================================\n")
        print("登录完成,开始轮询，现在进入到要学习的多个课程开始学习吧")
        print("完成开启学习界面以后，可以将浏览器窗口化成不影响工作的大小后最小化")
        print("软件轮询时可能会自动跳出")
        print("================================\n")
        break



def play():
    global autop
    #driver.set_window_size(300,200)
    all_handles=driver.window_handles
    missionlist=[]
    for i in all_handles:
        mission=""
        try:
            driver.switch_to.window(i)
            driver.find_element_by_xpath('//*[@title="播放"]').click()
            driver_title=str(driver.title)
            print(str(datetime.datetime.now())+"|"+driver_title+"|已恢复播放")
        except:
            time.sleep(0.1)
        if(autop==False):
            try:
                e=driver.find_element_by_xpath('//*[@class="required focus"]')
                if('已完成' in e.get_attribute("innerHTML")):
                    driver_title=str(driver.title)
                
                    try:
                        t=0
                        k=driver.find_elements_by_xpath('//*[@data-sectiontype>=1]')
                        for i in k:
                            if(i.get_attribute("class")=="required focus"):
                                k[t+1].click()
                                print(str(datetime.datetime.now())+"|"+driver_title+"|自动换P")
                                break
                            t=t+1
                    except Exception as e:
                        time.sleep(0.1)

            except:
                time.sleep(0.01)
        
        try:
            k=driver.find_elements_by_xpath('//*[@data-sectiontype>=1]')
            t=1
            outmode=""
            for i in k:
                if(i.get_attribute("class")=="required focus"):
                    if('已完成' in i.get_attribute("innerHTML")):
                        outmode="[已完成]"
                    elif('学习中' in i.get_attribute("innerHTML")):
                        outmode="[学习中]"
                    break
                t=t+1
            try:
                
                gettime1=driver.find_element_by_xpath('//*[@class="vjs-duration-display"]').get_attribute("innerHTML").replace('<span class="vjs-control-text">时长</span>',"")
                gettime2=driver.find_element_by_xpath('//*[@class="vjs-current-time-display"]').get_attribute("innerHTML").replace('<span class="vjs-control-text">当前时间</span>',"")
                if(gettime1!=""):
                    outmode=outmode+"[视频:{}/{}]".format(gettime2,gettime1)
            except Exception as e:
                outmode=outmode
            mission="["+str(t)+"/"+str(len(k))+"]"+outmode+driver.title
            #print(mission)
            if (len(k)!=0):
                missionlist.append(mission)
        except Exception as e:
            #print(e)
            time.sleep(0.01)
    return(missionlist)
outlist=[]
layout2=[
    [sg.Text("下次轮询时间")],
    [sg.Text("获取中",key='text',text_color='white')],
    [sg.Button("模式切换")],
    [sg.Button("测试模式")],
    [sg.Button("自动换P开关")],
    [sg.Text("当前任务",text_color='white')],
    [sg.Listbox(values=outlist,key='mission',size=(50,10))]
]
window= sg.Window('书山有路勤为径，学海无涯苦作舟', layout2,size=(500,300))
print("正在运行中，请不要退出窗口：")
timer=0
starttime=time.time()
while True:
    event,value = window.Read(timeout=1)
    nowtime=time.time()
    timer=nowtime-starttime
    window['text'].update(str(-timer+waittime))
    if(timer>waittime):
       outlist=play()
       driver.minimize_window()
       starttime=time.time()
       window['mission'].update(outlist)
    if(event==WIN_CLOSED):
        exit()
    if(event=="模式切换"):
        if(waittime==200):
            print("已切换到挂机模式")
            waittime=60
        else:
            print("已切换到工作模式")
            waittime=200
    if(event=="自动换P开关"):
        autop=not autop
        print(autop)
    if(event=="测试模式"):
        if(waittime==200):
            print("已切换到测试模式")
            waittime=10
        else:
            print("已切换到工作模式")
            waittime=200    