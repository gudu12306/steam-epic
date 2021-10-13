import win32clipboard as w
import win32con
import win32api
import win32gui
import ctypes
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

#把文字放入剪贴板
def setText(aString):
	w.OpenClipboard()
	w.EmptyClipboard()
	w.SetClipboardData(win32con.CF_UNICODETEXT,aString)
	w.CloseClipboard()
	
#模拟ctrl+V
def ctrlV():
	win32api.keybd_event(17,0,0,0) #ctrl
	win32api.keybd_event(86,0,0,0) #V
	win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0)#释放按键
	win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
	
#模拟alt+s
def altS():
	win32api.keybd_event(18,0,0,0)
	win32api.keybd_event(83,0,0,0)
	win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
# 模拟enter
def enter():
	win32api.keybd_event(13,0,0,0)
	win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
#模拟单击
def click():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#移动鼠标的位置
def movePos(x,y):
	win32api.SetCursorPos((x,y))

def get_free():
	url='https://steamstats.cn/xi'
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}
	r=requests.get(url,headers=headers)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	soup = BeautifulSoup(r.text, "html.parser")
	tbody=soup.find('tbody')
	tr=tbody.find_all('tr')
	i=1
	text="今日喜加一"+'\n'
	for tr in tr:
		td=tr.find_all('td')
		name=td[1].string.strip().replace('\n', '').replace('\r', '')
		gametype=td[2].string.replace(" ","").replace('\n', '').replace('\r', '')
		start=td[3].string.replace(" ","").replace('\n', '').replace('\r', '')
		end=td[4].string.replace(" ","").replace('\n', '').replace('\r', '')
		time=td[5].string.replace(" ","").replace('\n', '').replace('\r', '')
		oringin=td[6].find('span').string.replace(" ","").replace('\n', '').replace('\r', '')
		text=text+"序号："+str(i)+'\n'+"游戏名称："+name+'\n'+"DLC/game："+gametype+'\n'+"开始时间："+start+'\n'+"结束时间："+end+'\n'+"是否永久："+time+'\n'+"平台："+oringin+'\n'
	return text

if __name__=="__main__":
	target_a=['7:55']
	target_b=['8:00']
	name_list=['Squirrel C']
	while True:
		now=time.strftime("%m月%d日%H:%M",time.localtime())
		print(now)
		if now[-5:] in target_a:
			text=get_free()
		if now[-5:] in target_b:
			hwnd=win32gui.FindWindow("WeChatMainWndForPC", '微信')
			win32gui.ShowWindow(hwnd,win32con.SW_SHOW)
			win32gui.MoveWindow(hwnd,0,0,1000,700,True)
			time.sleep(1)
			for name in name_list:
				movePos(28,147)
				click()
				#2.移动鼠标到搜索框，单击，输入要搜索的名字
				movePos(148,35)
				click()
				time.sleep(1)
				setText(name)
				ctrlV()
				time.sleep(1)  # 等待联系人搜索成功
				enter()
				time.sleep(1)
				now=time.strftime("%m月%d日%H:%M",time.localtime())
				text='现在是'+now+'\n'+text
				setText(text)
				ctrlV()
				time.sleep(1)
				altS()
				time.sleep(1)
			win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
		time.sleep(60)

