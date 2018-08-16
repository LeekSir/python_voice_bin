import glob
import sys
import os
import os.path
import struct
import re

#读单个音频文件的函数
def read_voice_file(fileName,bin):
	try:
		voice = open(fileName,'rb+')
		
		voice.seek(0)
		pos_start = voice.tell()
		for line in voice.readlines():
			pass
		pos_end = voice.tell()
		#看是否四字对齐
		sup = 4 - ((pos_end - pos_start) % 4)
		while sup > 0 and sup != 4:
			voice.write(struct.pack('B', int('0', 16)))
			sup -= 1
			
		voice.seek(0)
		for line in voice.readlines():
			v_bin.write(line)
	finally:
		if voice:
			voice.close()

#main 函数开始
voice_p = input('Please input voice path:')
files = os.listdir(voice_p)
fileNames = []
fileNames2 = []
index_p = {}
flag = 0
vp = 0
p = 0x830000 + 0x44#index address  0x44 = 68 0x64 = 100 

try:
	v_bin = open('voice.bin','wb')
	v_bin.seek(0x44)
	vp_start, vp_end = 0, 0
	if voice_p:
		print('path: %s!' % voice_p)
		for fileName in files:
			fileNames.append(int(fileName.split('.')[0]))
		fileNames.sort()
		for f in fileNames:
			fileNames2.append(voice_p + '/' + str(f) + '.bin')
		for fileName in fileNames2:
			p += vp
			index_p[fileName.split('/')[2]] = hex(p)
			vp_start = v_bin.tell()
			read_voice_file(fileName,v_bin)
			vp_end = v_bin.tell()
			vp = vp_end - vp_start
		
		#将index写入index.txt文件
		try:
			index_f = open('index.txt', 'w')
			for k in index_p:
				print(k + ': ' + index_p[k])
				index_str = str(k) +':' + str(index_p[k]) + '\n'
				index_f.writelines(index_str)
		finally:
			if index_f:
				index_f.close()
			
		v_bin.seek(0)
		
		for k in index_p:
			index = []
			i = 0
			while i < 4: 
				index.append(re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str(index_p[k])).split(' ')[i])
				i += 1
				
			flag = True
			for i in index:
				if flag:
					flag = False
					continue
				a = struct.pack('B', int(i, 16))
				v_bin.write(a)
				
			v_bin.seek(v_bin.tell()+1)
	else:
		print('NO voice path!')
finally:
	if v_bin:
		v_bin.close()