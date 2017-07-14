#coding = utf-8

from django import forms
from django.http import HttpResponse as hr
from django.template.loader import render_to_string as rts
from django.shortcuts import render as rd
import base64 as b
import os

err = {
	"m":"用户名或密码错误！"
}

bpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def post(rq):
	print(len(rq.POST))
	if len(rq.POST) != 0:
		if ('u' in rq.POST) and ('p' in rq.POST) and ((rq.POST['u'] != "team9071.cn") or (rq.POST['p'] != 'Kaifarizhi@9071')):
			return rd(rq,"index.html",err)
		elif ('title' in rq.POST) and ('date' in rq.POST) and ('content' in rq.POST):
			num = 0
			plist = []
			nlist = []
			path = False
			for p,d,f in os.walk('.\\upload\\'):
				if not path:
					path = True
					plist = d
			for n in plist:
				nlist.append(int(n))
			nlist.sort()
			nu = (0 if len(nlist) is 0 else nlist[len(nlist)-1])
			num = int(nu) + 1
			if not os.path.exists(os.path.join(bpath,'upload\\'+str(num)+'\\')):
				os.makedirs(os.path.join(bpath,'upload\\'+str(num)+'\\'))
			f = open('.\\upload\\'+str(num)+'\\text.txt','w',encoding="utf8")
			img = None
			ipath = ''
			tpath = '已将文本保存于    .\\upload\\'+str(num)+'\\text.txt'
			if rq.POST['imgb64'] != '':
				#print(rq.POST['imgb64'].split("base64,"))
				img = b.b64decode(rq.POST['imgb64'].split("base64,")[1])
				im = open('.\\upload\\'+str(num)+"\\image."+rq.POST['ext'],"wb")
				ipath = "已将图片保存于    " + '.\\upload\\' + str(num) + "\\image." + rq.POST['ext']
				#print("Image saved as " + '.\\upload\\' + str(num) + "\\image." + rq.POST['ext'])
				im.write(img)
				im.close()
			c = []
			c.append("title:"+rq.POST['title']+'\n')
			c.append("date:"+rq.POST['date']+'\n')
			c.append("content:"+rq.POST['content']+'\n')
			f.writelines(c)
			pm = {
				"ipath":ipath,
				"tpath":tpath,
			}
			return rd(rq,"success.html",pm)
		else:
			return rd(rq,"submit.html")
	return rd(rq,"index.html")