__author__ = 'Tianyu Dai (dtysky)'

from PIL import Image
import os, json
from ctypes import *
from RowsGenerator import RowsGenerator as RG
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

FileFormat = ['.jpg', '.bmp']
Conf = json.load(open('../ImageForTest/conf.json', 'r'))['conf']

def show_error(e):
	MessageBox(e)
	exit(0)

def name_format(root, name, ex, conf):
	return '%s-%s' % (name, conf['width'])

def conf_format(im, conf):
	return '%s\n%d\n' % (im.mode, conf['width'])

def color_format(mode, color):
	if mode == '1':
		return '0' if color == 0 else '1'
	color = [color]
	res = ''
	for c in color:
		tmp = bin(c)[2:]
		for i in xrange(10 - len(bin(c))):
			tmp = '0' + tmp
		res += tmp
	return res

def create_dat(im, conf):
	mode = im.mode
	xsize, ysize = im.size
	if mode not in ['L', '1']:
		show_error('Simulations for this module just supports Gray-scale and binary images, check your images !')
	if xsize != 512:
		show_error('Simulations for this module just supports 512xN images, check your images !')
	if conf['width'] not in [3, 5]:
		show_error('''Simulations for this module just supports conf "width" 3 and 5, check your images !''')
	rows = RG(im, conf['width'])
	data_res = ''
	while not rows.frame_empty():
		row = rows.update()
		row.reverse()
		for p in row:
			if mode == '1':
				p = 0 if p == 0 else 1
			data_res += color_format(mode, p)
		data_res += '\n'
	return data_res[:-1]

FileAll = []
for root,dirs,files in os.walk('../ImageForTest'):
    for f in files:
    	name, ex=os.path.splitext(f)
        if ex in FileFormat:
        	FileAll.append((root+'/', name, ex))
dat_index = ''
for root, name, ex in FileAll:
	im_src = Image.open(root + name + ex)
	xsize, ysize = im_src.size
	for c in Conf:
		dat_res = open('../FunSimForHDL/%s.dat' \
			% name_format(root, name, ex, c), 'w')
		dat_res.write('%d\n%d\n' % (xsize, ysize))
		dat_res.write('%s' % conf_format(im_src, c))
		dat_res.write(create_dat(im_src, c))
		dat_index += '%s' % name_format(root, name, ex, c)
		dat_index += '\n'
		dat_res.close()
dat_index = dat_index[:-1]
dat_index_f = open('../FunSimForHDL/imgindex.dat','w')
dat_index_f.write(dat_index)
dat_index_f.close()