#coding:utf-8
import sys
import tkinter as tk
import random
from PIL import Image, ImageDraw, ImageTk
from tkinter import messagebox
import time
# click時のイベント
hand = []
hand_prce = []
side = []
trash_card = []
images = []  # to hold the newly created image
active_len = []
count_len_0 = []
count_len_1 = []
count_len_2 = []
count_len_3 = []
count_len_4 = [] 
### ここにイベントが発生したときの処理 ###
pressed_x = pressed_y = 0
item_id = -1
tag = "img"
click_num = 0
benchx = 198
active_pokemon_in = 0
bench_pokemon_in = []
bench_pokemon_num = 0
tag_save = 0
active_pokemon_en = {}
bench_pokemon_en_0 = {}
bench_pokemon_en_1 = {}
bench_pokemon_en_2 = {}
bench_pokemon_en_3 = {}
bench_pokemon_en_4 = {}
active_pokemon_en_placex = 362
bench_pokemon_en_0_placex = 160
bench_pokemon_en_1_placex = 261
bench_pokemon_en_2_placex = 362
bench_pokemon_en_3_placex = 463
bench_pokemon_en_4_placex = 564
trash_num = 0
deck_card_choice = ""

#def card_mouseover(event):
#	global canvas, tag
#	tag_card_mouseover = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(event.x,event.y,event.x,event.y)]
#	print(tag_card_mouseover[-2])
#	canvas.move(tag_card_mouseover[-2],0,-5)

#マウスにカードがついてくる処理
def motion(event):
	global canvas, tag
	canvas.coords(tag, event.x, event.y)

def place_pressed(event):
	global tag, click_num, card_cx, tag_del
	tag = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(event.x,event.y,event.x,event.y)]
	if len(tag) == 2:
		return
	else:
		tag = tag[-2]
	
	if click_num == 0:
		canvas.bind("<Motion>", motion)
		click_num = 1
		tag_del = tag
	elif click_num == 1:
		canvas.delete(tag_del)
		card_c = tag_del.replace('img', '')
		card_cx = int(card_c) * 15 + 50
		canvas.create_image(card_cx, 510, image=hand[int(card_c)], tags=tag_del)
		card_c = int(card_c) + 1
		if not len(hand) == card_c:
			canvas.tag_lower(tag_del, "img" + str(card_c))
		canvas.unbind("<Motion>")
		canvas.tag_raise("hand_place")
		click_num = 0

#バトル場の当たり判定に触れた
def active_place_in(event):
	canvas.tag_raise("active_place")
	canvas.tag_bind("active_place","<ButtonPress-1>",active_place_click)

#バトル場に関係する処理
def active_place_click(event):
	global click_num, tag_del, tag, hand_prce, active_pokemon_in, active_pokemon_en_placex
	if click_num == 1:
		card_c = tag_del.replace('img', '')
		types = hand_prce[int(card_c)].split('_')[0]
		if len(bench_pokemon_in) < 5 and types == "P":#バトル場にポケモンを出す
			card_c = tag_del.replace('img', '')
			types = hand_prce[int(card_c)].split('_')[1]
			print(types)
			if types == "0" and active_pokemon_in == 0:
				canvas.delete(tag_del)
				active_pokemon = hand[int(card_c)]
				hand.pop(int(card_c))
				hand_prce.pop(int(card_c))
				print(active_pokemon)
				canvas.unbind("<Motion>")
				click_num = 0
				canvas.create_image(400, 130, image=active_pokemon, tags="activ_pokemon")
				hand_sort()
				fast_side()
				btn2 = tk.Button(root, text='カードを引く',command = btn_click2) # ボタンの設定(text=ボタンに表示するテキスト)
				btn2.place(x=687, y=130) #ボタンを配置する位置の設定
				active_pokemon_in = 1
				
		elif types == "Gen" or types == "Firen" or types == "Wen" or types == "Een" or types == "Pen" or types == "Figen" or types == "Daen" or types == "Sen" or types == "Faien":#バトルポケモンにエネルギーをつける
			tag_en = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(event.x,event.y,event.x,event.y)]
			card_c = tag_del.replace('img', '')
			if tag_en[-3] == "activ_pokemon":
				if not types in active_pokemon_en:
					energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
					energie_image = energie_image.resize((20, 20))
					energie_image = ImageTk.PhotoImage(energie_image)
					canvas.create_image(active_pokemon_en_placex, 185, image=energie_image, tag=types + str(len(active_pokemon_en)))
					active_pokemon_en[types] = [types + "0"]
					active_pokemon_en_placex += 20
					hand.pop(int(card_c))
					hand_prce.pop(int(card_c))
					canvas.unbind("<Motion>")
					click_num = 0
					hand_sort()
					print(active_pokemon_en)
				elif len(active_pokemon_en) > 0:
					active_pokemon_en_count = 362
					active_len.clear()
					active_pokemon_en_put = active_pokemon_en[types]
					active_pokemon_en_put.insert(0,types + str(len(active_pokemon_en[types])))
					active_pokemon_en[types] = active_pokemon_en_put
					hand.pop(int(card_c))
					hand_prce.pop(int(card_c))
					canvas.unbind("<Motion>")
					click_num = 0
					hand_sort()
					for typecount in active_pokemon_en:
						encount = len(active_pokemon_en[typecount])
						count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
						count = count.resize((20, 20))
						count = ImageTk.PhotoImage(count)
						active_len.append(count)
						canvas.delete("active_ene_counter")
					for counter in range(len(active_len)):
						canvas.create_image(active_pokemon_en_count, 185, image=active_len[counter], tag="active_ene_counter")
						active_pokemon_en_count += 20
		elif types == "g" or types == "su" or types == "pg" or types == "st":#トレーナーズを出す
			trainers()
		else:
			print("たねポケモンしか出せません。")
	root.mainloop()
	
	#トレーナーズの処理
def trainers():
	global click_num, tag_del, active_pokemon_in, card_full_name
	canvas.delete("g_su_st")
	print(tag_del)
	card_c = tag_del.replace('img', '')
	card_full_name = hand_prce[int(card_c)]
	types = hand_prce[int(card_c)].split('_')[-1].replace('.png', '')
	trainers = hand[int(card_c)]
	print(trainers)
	canvas.create_image(550, 130, image=trainers, tag="g_su_st")
	hand.pop(int(card_c))
	hand_prce.pop(int(card_c))
	canvas.unbind("<Motion>")
	click_num = 0
	hand_sort()
	if types == "クイックボール":
		print("トラッシュするカードを選んでください。")
		canvas.tag_bind("hand_place", "<ButtonPress-1>", card_effect_trash)
	root.mainloop()
		
#手札からカードを捨てる
def card_effect_trash(event):
	global tag, click_num, card_cx, tag_del, tag_save, trash_num, deck_card_choice
	tag = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(event.x,event.y,event.x,event.y)]
	print(tag)
	tag_del = tag[-2]
	card_c = tag_del.replace('img', '')
	print(tag_save)
	print(tag[-2])
	
	if trash_num == 0:#カードを1枚捨てる
		tag_save = tag[-2]
		canvas.move(tag_save,0,-10)
		trash_num = 1
	elif not tag_save == tag[-2]:
		print("hfurpe")
		canvas.move(tag_save,0,10)
		tag_save = tag[-2]
		canvas.move(tag_save,0,-10)
	elif tag[-2] == tag_save:
		trash_card.insert(0,hand[int(card_c)])
		print(trash_card)
		hand.pop(int(card_c))
		hand_prce.pop(int(card_c))
		hand_sort()
		deck_card_choice = "P"
		deck_check()
	
#ベンチの当たり判定に触れた
def bench_Place_in(event):
	canvas.tag_raise("bench_Place")
	canvas.tag_bind("bench_Place","<ButtonPress-1>",bench_Place_click)

#ベンチに関係する処理
def bench_Place_click(event):
	global click_num, tag_del, tag, hand_prce, bench_pokemon_in, bench_pokemon_num, benchx, bench_pokemon_en_0, bench_pokemon_en_1, bench_pokemon_en_2, bench_pokemon_en_3, bench_pokemon_en_4, bench_pokemon_en_0_placex, bench_pokemon_en_1_placex, bench_pokemon_en_2_placex, bench_pokemon_en_3_placex, bench_pokemon_en_4_placex, active_pokemon_in
	if active_pokemon_in == 1:
		if click_num == 1:
			card_c = tag_del.replace('img', '')
			types = hand_prce[int(card_c)].split('_')[0]
			if len(bench_pokemon_in) < 5 and types == "P":#ポケモンをベンチに出す
				card_c = tag_del.replace('img', '')
				types = hand_prce[int(card_c)].split('_')[1]
				if types == "0":
					canvas.delete(tag_del)
					bench_pokemon_in.insert(0,hand[int(card_c)])
					bench_pokemon = bench_pokemon_in[0]
					canvas.create_image(benchx, 310, image=bench_pokemon, tags="bench_pokemon["+str(bench_pokemon_num)+"]")
					benchx = benchx + 101
					hand.pop(int(card_c))
					hand_prce.pop(int(card_c))
					canvas.unbind("<Motion>")
					click_num = 0
					bench_pokemon_num += 1
					hand_sort()
					root.mainloop()
			elif types == "Gen" or types == "Firen" or types == "Wen" or types == "Een" or types == "Pen" or types == "Figen" or types == "Daen" or types == "Sen" or types == "Faien":#ベンチポケモンにエネルギーをつける
				tag_en = [canvas.itemcget(obj, 'tags') for obj in canvas.find_overlapping(event.x,event.y,event.x,event.y)]
				card_c = tag_del.replace('img', '')
			
				if tag_en[-3] == "bench_pokemon[0]":
					if not types in bench_pokemon_en_0:
						energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
						energie_image = energie_image.resize((20, 20))
						energie_image = ImageTk.PhotoImage(energie_image)
						canvas.create_image(bench_pokemon_en_0_placex, 365, image=energie_image, tag=types + str(len(bench_pokemon_en_0)))
						bench_pokemon_en_0[types] = [types + "0"]
						bench_pokemon_en_0_placex += 20
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						print(bench_pokemon_en_0)
					elif len(bench_pokemon_en_0) > 0:
						bench_pokemon_en_0_count = 160
						count_len_0.clear()
						bench_pokemon_en_0_put = bench_pokemon_en_0[types]
						bench_pokemon_en_0_put.insert(0,types + str(len(bench_pokemon_en_0[types])))
						bench_pokemon_en_0[types] = bench_pokemon_en_0_put
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						for typecount in bench_pokemon_en_0:
							encount = len(bench_pokemon_en_0[typecount])
							count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
							count = count.resize((20, 20))
							count = ImageTk.PhotoImage(count)
							count_len_0.append(count)
							canvas.delete("ene_counter0")
						for counter in range(len(count_len_0)):
							canvas.create_image(bench_pokemon_en_0_count, 365, image=count_len_0[counter], tag="ene_counter0")
							bench_pokemon_en_0_count += 20
								
				elif tag_en[-3] == "bench_pokemon[1]":
					if not types in bench_pokemon_en_1:
						energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
						energie_image = energie_image.resize((20, 20))
						energie_image = ImageTk.PhotoImage(energie_image)
						canvas.create_image(bench_pokemon_en_1_placex, 365, image=energie_image, tag=types + str(len(bench_pokemon_en_1)))
						bench_pokemon_en_1[types] = [types + "0"]
						bench_pokemon_en_1_placex += 20
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						print(bench_pokemon_en_1)
					elif len(bench_pokemon_en_1) > 0:
						bench_pokemon_en_1_count = 261
						count_len_1.clear()
						bench_pokemon_en_1_put = bench_pokemon_en_1[types]
						bench_pokemon_en_1_put.insert(0,types + str(len(bench_pokemon_en_1[types])))
						bench_pokemon_en_1[types] = bench_pokemon_en_1_put
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						for typecount in bench_pokemon_en_1:
							encount = len(bench_pokemon_en_1[typecount])
							count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
							count = count.resize((20, 20))
							count = ImageTk.PhotoImage(count)
							count_len_1.append(count)
							canvas.delete("ene_counter1")
						for counter in range(len(count_len_1)):
							canvas.create_image(bench_pokemon_en_1_count, 365, image=count_len_1[counter], tag="ene_counter1")
							bench_pokemon_en_1_count += 20
							
				elif tag_en[-3] == "bench_pokemon[2]":
					if not types in bench_pokemon_en_2:
						energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
						energie_image = energie_image.resize((20, 20))
						energie_image = ImageTk.PhotoImage(energie_image)
						canvas.create_image(bench_pokemon_en_2_placex, 365, image=energie_image, tag=types + str(len(bench_pokemon_en_2)))
						bench_pokemon_en_2[types] = [types + "0"]
						bench_pokemon_en_2_placex += 20
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						print(bench_pokemon_en_2)
					elif len(bench_pokemon_en_2) > 0:
						bench_pokemon_en_2_count = 362
						count_len_2.clear()
						bench_pokemon_en_2_put = bench_pokemon_en_2[types]
						bench_pokemon_en_2_put.insert(0,types + str(len(bench_pokemon_en_2[types])))
						bench_pokemon_en_2[types] = bench_pokemon_en_2_put
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						for typecount in bench_pokemon_en_2:
							encount = len(bench_pokemon_en_2[typecount])
							count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
							count = count.resize((20, 20))
							count = ImageTk.PhotoImage(count)
							count_len_2.append(count)
							canvas.delete("ene_counter2")
						for counter in range(len(count_len_2)):
							canvas.create_image(bench_pokemon_en_2_count, 365, image=count_len_2[counter], tag="ene_counter2")
							bench_pokemon_en_2_count += 20
					
				elif tag_en[-3] == "bench_pokemon[3]":
					if not types in bench_pokemon_en_3:
						energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
						energie_image = energie_image.resize((20, 20))
						energie_image = ImageTk.PhotoImage(energie_image)
						canvas.create_image(bench_pokemon_en_3_placex, 365, image=energie_image, tag=types + str(len(bench_pokemon_en_3)))
						bench_pokemon_en_3[types] = [types + "0"]
						bench_pokemon_en_3_placex += 20
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						print(bench_pokemon_en_3)
					elif len(bench_pokemon_en_3) > 0:
						bench_pokemon_en_3_count = 463
						count_len_3.clear()
						bench_pokemon_en_3_put = bench_pokemon_en_3[types]
						bench_pokemon_en_3_put.insert(0,types + str(len(bench_pokemon_en_3[types])))
						bench_pokemon_en_3[types] = bench_pokemon_en_3_put
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						for typecount in bench_pokemon_en_3:
							encount = len(bench_pokemon_en_3[typecount])
							count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
							count = count.resize((20, 20))
							count = ImageTk.PhotoImage(count)
							count_len_3.append(count)
							canvas.delete("ene_counter3")
						for counter in range(len(count_len_3)):
							canvas.create_image(bench_pokemon_en_3_count, 365, image=count_len_3[counter], tag="ene_counter3")
							bench_pokemon_en_3_count += 20
			
				elif tag_en[-3] == "bench_pokemon[4]":
					if not types in bench_pokemon_en_4:
						energie_image = Image.open("/Users/hw18a153/Desktop/エネルギー/"+types+".png")
						energie_image = energie_image.resize((20, 20))
						energie_image = ImageTk.PhotoImage(energie_image)
						canvas.create_image(bench_pokemon_en_4_placex, 365, image=energie_image, tag=types + str(len(bench_pokemon_en_4)))
						bench_pokemon_en_4[types] = [types + "0"]
						bench_pokemon_en_4_placex += 20
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						print(bench_pokemon_en_4)
					elif len(bench_pokemon_en_4) > 0:
						bench_pokemon_en_4_count = 564
						count_len_4.clear()
						bench_pokemon_en_4_put = bench_pokemon_en_4[types]
						bench_pokemon_en_4_put.insert(0,types + str(len(bench_pokemon_en_4[types])))
						bench_pokemon_en_4[types] = bench_pokemon_en_4_put
						hand.pop(int(card_c))
						hand_prce.pop(int(card_c))
						canvas.unbind("<Motion>")
						click_num = 0
						hand_sort()
						for typecount in bench_pokemon_en_4:
							encount = len(bench_pokemon_en_4[typecount])
							count = Image.open("/Users/hw18a153/Desktop/エネルギー/%s.png" % encount)
							count = count.resize((20, 20))
							count = ImageTk.PhotoImage(count)
							count_len_4.append(count)
							canvas.delete("ene_counter4")
						for counter in range(len(count_len_4)):
							canvas.create_image(bench_pokemon_en_4_count, 365, image=count_len_4[counter], tag="ene_counter4")
							bench_pokemon_en_4_count += 20
				root.mainloop()
			else:
				print("ベンチは5匹までです。")

#手札を並べる
def hand_sort():
	global hand
	posx = 50
	if len(hand) >= 0:
		for delete in range(len(hand) + 1):
			card_del = "img" + str(delete)
			canvas.delete(card_del)
	for handcard in range(len(hand)):
		card_tag = "img" + str(handcard)
		canvas.create_image(posx, 510, image=hand[handcard], tags=card_tag)
		posx = posx + 15
	canvas.tag_raise("hand_place")
		
#def deck_card_move(id,x,y):
	
#サイドを並べる
def fast_side():
	print("サイドを並べました。")
	for _ in range(6):
		cardimage = Image.open("/Users/hw18a153/Desktop/pokemon_img/%s" % l[0])
		card = cardimage.resize((90, 125))
		card = ImageTk.PhotoImage(card)
		side.insert(0,card)
		l.pop(0)
	canvas.create_image(20, 17, image=card_ura_image, anchor=tk.NW)
	canvas.create_image(20, 146, image=card_ura_image, anchor=tk.NW)
	canvas.create_image(20, 274, image=card_ura_image, anchor=tk.NW)
	canvas.create_image(40, 6, image=card_ura_image, anchor=tk.NW)
	canvas.create_image(40, 135, image=card_ura_image, anchor=tk.NW)
	canvas.create_image(40, 263, image=card_ura_image, anchor=tk.NW)

#開始時のカードを7枚引く
def btn_click1():
	print("7枚引きました。")
	btn1.config(state="disable")
	for _ in range(7):
		cardimage = Image.open("/Users/hw18a153/Desktop/pokemon_img/%s" % l[0])
		hand_prce.insert(0,l[0])
		print(hand_prce)
		card = cardimage.resize((90, 125))
		card = ImageTk.PhotoImage(card)
		hand.insert(0,card)
		posx = 50
		if len(hand) > 0:
			for delete in range(len(hand)):
				card_del = "img" + str(delete)
				canvas.delete(card_del)
		for handcard in range(len(hand)):
			card_tag = "img" + str(handcard)
			canvas.create_image(posx, 510, image=hand[handcard], tags=card_tag)
			posx = posx + 15
		l.pop(0)
	for marigan in range(len(hand_prce)):#手札にポケモンがいない時の処理
		card_f = hand_prce[marigan].split('_')[0]
		if card_f == "P":
			break
		elif marigan == 6:
			print("ポケモンがいませんでした。")
			time.sleep(0.5)
			print("くりなおします。")
			time.sleep(0.5)
			for marigan in range(len(hand)):
				l.insert(0,hand_prce[0])
				hand_prce.pop(0)
			random.shuffle(l)
			hand.clear()
			btn_click1()
			
	canvas.tag_raise("hand_place")
	print("バトル場にたねポケモンを出してください。")
	root.mainloop()

#カードを1枚引く
def btn_click2():
	print("カードを引く")
	cardimage = Image.open("/Users/hw18a153/Desktop/pokemon_img/%s" % l[0])
	hand_prce.insert(0,l[0])
	print(hand_prce)
	card = cardimage.resize((90, 125))
	card = ImageTk.PhotoImage(card)
	hand.insert(0,card)
	posx =  50
	if len(hand) > 0:
		for delete in range(len(hand)):
			card_del = "img" + str(delete)
			canvas.delete(card_del)
	for handcard in range(len(hand)):
		card_tag = "img" + str(handcard)
		canvas.create_image(posx, 510, image=hand[handcard], tags=card_tag)
		posx = posx + 15
	l.pop(0)
	canvas.tag_raise("hand_place")
	root.mainloop()

#トラッシュの確認のウィンドウを閉じる
def btn_click3():
	global root2
	root2.destroy()

#デッキの確認のウィンドウを閉じる
def btn_click4():
	global root3, tags, card_image_trash, canvas, tag, click_num, trainers
	hand_prce.insert(0,l[int(tags)])
	l.pop(int(tags))
	card_image = card_image_trash[int(tags)]
	card_image = card_image.resize((90, 125))
	card_image = ImageTk.PhotoImage(card_image)
	hand.insert(0,card_image)
	random.shuffle(l)
	hand_sort()
	root3.destroy()
	canvas.tag_bind("hand_place", "<ButtonPress-1>", place_pressed)
	click_num = 0
	trash_card.insert(0,trainers)
	canvas.delete("g_su_st")
	root.mainloop()

#透明な当たり判定の箱を作る
def create_rectangle(x1, y1, x2, y2, **kwargs):
	if 'alpha' in kwargs:
		alpha = int(kwargs.pop('alpha') * 255)
		fill = kwargs.pop('fill')
		fill = root.winfo_rgb(fill) + (alpha,)
		image = Image.new('RGBA', (x2-x1, y2-y1), fill)
		images.append(ImageTk.PhotoImage(image))
		canvas.create_image(x1, y1, image=images[-1], anchor='nw')
	canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

#トラッシュの内容を確認する
def trash_check(event):
	global root2, trash_card
	root2 = tk.Tk()
	root2.title(u"トラッシュ")
	root2.geometry("535x500")
	canvas3 = tk.Canvas(root2, width=550, height=500)
	canvas3.place(x=0, y=0)
	btn3 = tk.Button(root2, text='閉じる',command = btn_click3) # ボタンの設定(text=ボタンに表示するテキスト)
	btn3.place(x=475, y=465) #ボタンを配置する位置の設定
	card_image_palcex = 30
	card_image_palcey = 40
	counter_cou = 10
	counter_cou_cou = 0
	print(trash_card)
	for trash_draw in range(len(trash_card)):
		counter_cou_cou += 1
		canvas3.create_image(card_image_palcex, card_image_palcey, image=trash_card[trash_draw], tag="img"+str(trash_draw)+"")
		card_image_palcex += 53
		print(trash_draw)
		if counter_cou_cou == counter_cou:
			print("njubfpivlfs")
			card_image_palcey += 74
			card_image_palcex = 30
			counter_cou += 10
			
			
	#canvas3.bind("<ButtonPress-1>", trash_check_click)
	
	root2.mainloop()

#デッキの内容を確認する
def deck_check():
	global root3, tag, canvas2, deck_strage, card_image_l, btn4, card_image_trash
	root3 = tk.Tk()
	root3.title(u"デッキ")
	root3.geometry("535x500")
	canvas2 = tk.Canvas(root3, width=550, height=500)
	canvas2.place(x=0, y=0)
	#btn4 = tk.Button(root3, text='閉じる',command = btn_click4) # ボタンの設定(text=ボタンに表示するテキスト)
	#btn4.place(x=475, y=465) #ボタンを配置する位置の設定
	btn4 = tk.Button(root3, text='このカードを手札に加える',command = btn_click4)
	btn4.place(x=350, y=465)
	btn4.config(state="disable")
	card_image_palcex = 30
	card_image_palcey = 40
	counter_cou = 10
	counter_cou_cou = 0
	card_image_l = []
	card_image_trash = []
	for deck_strage in l:
		card_image = Image.open("/Users/hw18a153/Desktop/pokemon_img/"+deck_strage+"")
		card_image_trash.append(card_image)
		card_image = card_image.resize((52, 73))
		card_image = ImageTk.PhotoImage(card_image,master = root3)
		card_image_l.append(card_image)
	for deck_draw in range(len(card_image_l)):
		counter_cou_cou += 1
		canvas2.create_image(card_image_palcex, card_image_palcey, image=card_image_l[deck_draw], tag="img"+str(deck_draw)+"")
		card_image_palcex += 53
		print(deck_draw)
		if counter_cou_cou == counter_cou:
			print("njubfpivlfs")
			card_image_palcey += 74
			card_image_palcex = 30
			counter_cou += 10
			
			
	canvas2.bind("<ButtonPress-1>", deck_check_click)
	
	root3.mainloop()
	
#デッキ内のカードを選択する
def deck_check_click(event):
	global canvas2, deck_strage, deck_card_choice, card_image_l, btn4, card_image_trash, tags, card_full_name
	tag = [canvas2.itemcget(obj, 'tags') for obj in canvas2.find_overlapping(event.x,event.y,event.x,event.y)]
	tags = tag[0].replace('img', '').replace(' current', '')
	print(card_image_l[int(tags)])
	print(tags)
	print(card_image_trash[int(tags)])
	check_card_type = l[int(tags)].split('_')[0]
	canvas2.delete("card_choi")
	print(l[int(tags)])
	canvas.tag_unbind("hand_place", "<ButtonPress-1>")
	if int(tags) < 10:
		x0 = 3 + 53 * int(tags)
		y0 = 4
		x1 = 55 + 53 * int(tags)
		y1 = 76
	else:
		x0 = 3 + 53 * int(tags[-1])
		y0 = 4 + 74 * int(tags[-2])
		x1 = 55 + 53 * int(tags[-1])
		y1 = 76 + 74 * int(tags[-2])
	
	canvas2.create_rectangle(x0, y0, x1, y1, outline="Red", width=3, tag="card_choi")#塗りつぶし
	if deck_card_choice == "P" and check_card_type == "P":
		btn4.config(state="normal")
	else:
		btn4.config(state="disable")

	
		

l = ['Wen_none_none_none_none_none_none_none_none_none_基本水エネルギー.png', 'Wen_none_none_none_none_none_none_none_none_none_基本水エネルギー.png', 'Wen_none_none_none_none_none_none_none_none_none_基本水エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'Sen_none_none_none_none_none_none_none_none_none_基本鋼エネルギー.png', 'st_none_none_none_none_none_none_none_none_none_トキワの森.png', 'st_none_none_none_none_none_none_none_none_none_トキワの森.png', 'su_none_none_none_none_none_none_none_none_none_とりつかい.png', 'su_none_none_none_none_none_none_none_none_none_マリィ.png', 'su_none_none_none_none_none_none_none_none_none_マリィ.png', 'su_none_none_none_none_none_none_none_none_none_マリィ.png', 'su_none_none_none_none_none_none_none_none_none_ボスの指令（サカキ）.png', 'su_none_none_none_none_none_none_none_none_none_ボスの指令（サカキ）.png', 'su_none_none_none_none_none_none_none_none_none_ボスの指令（サカキ）.png', 'su_none_none_none_none_none_none_none_none_none_ボスの指令（サカキ）.png', 'su_none_none_none_none_none_none_none_none_none_博士の研究（マグノリア博士）.png', 'su_none_none_none_none_none_none_none_none_none_博士の研究（マグノリア博士）.png', 'su_none_none_none_none_none_none_none_none_none_博士の研究（マグノリア博士）.png', 'su_none_none_none_none_none_none_none_none_none_博士の研究（マグノリア博士）.png', 'g_none_none_none_none_none_none_none_none_none_リセットスタンプ.png', 'g_none_none_none_none_none_none_none_none_none_リセットスタンプ.png', 'pg_none_none_none_none_none_none_none_none_none_くちたけん.png', 'g_none_none_none_none_none_none_none_none_none_ツールスクラッパー.png', 'g_none_none_none_none_none_none_none_none_none_グレートキャッチャー.png', 'pg_none_none_none_none_none_none_none_none_none_大きなおまもり.png', 'pg_none_none_none_none_none_none_none_none_none_大きなおまもり.png', 'g_none_none_none_none_none_none_none_none_none_プレシャスボール.png', 'g_none_none_none_none_none_none_none_none_none_プレシャスボール.png', 'g_none_none_none_none_none_none_none_none_none_ポケモンいれかえ.png', 'g_none_none_none_none_none_none_none_none_none_ポケモンいれかえ.png', 'g_none_none_none_none_none_none_none_none_none_ポケモンいれかえ.png', 'g_none_none_none_none_none_none_none_none_none_ポケモンいれかえ.png', 'g_none_none_none_none_none_none_none_none_none_エネルギーつけかえ.png', 'g_none_none_none_none_none_none_none_none_none_エネルギーつけかえ.png', 'g_none_none_none_none_none_none_none_none_none_エネルギーつけかえ.png', 'g_none_none_none_none_none_none_none_none_none_エネルギーつけかえ.png', 'g_none_none_none_none_none_none_none_none_none_メタルソーサー.png', 'g_none_none_none_none_none_none_none_none_none_メタルソーサー.png', 'g_none_none_none_none_none_none_none_none_none_メタルソーサー.png', 'g_none_none_none_none_none_none_none_none_none_メタルソーサー.png', 'g_none_none_none_none_none_none_none_none_none_クイックボール.png', 'g_none_none_none_none_none_none_none_none_none_クイックボール.png', 'g_none_none_none_none_none_none_none_none_none_クイックボール.png', 'g_none_none_none_none_none_none_none_none_none_クイックボール.png', 'P_0_V_none_180_G_1_Fir_none_0_ワタシラガV.png', 'P_0_V_none_180_Da_1_Fig_none_0_クロバットV.png', 'P_0_GX_none_170_S_1_Fir_P20_0_クチートGX.png', 'P_0_GX_none_170_S_1_Fir_P20_0_クチートGX.png', 'P_0_GX_none_160_E_1_Fig_S20_0_デデンネGX.png', 'P_0_GX_none_160_E_1_Fig_S20_0_デデンネGX.png', 'P_0_V_none_220_S_1_Fir_G30_0_ザシアンV.png', 'P_0_V_none_220_S_1_Fir_G30_0_ザシアンV.png', 'P_0_V_none_220_S_1_Fir_G30_0_ザシアンV.png', 'P_0_TAG TEAM_none_280_Dr_0_Fai_none_0_アルセウス&ディアルガ&パルキアGX.png', 'P_0_TAG TEAM_none_280_Dr_0_Fai_none_0_アルセウス&ディアルガ&パルキアGX.png']

random.shuffle(l)

root = tk.Tk()
root.title(u"メイン画面")
root.geometry("950x600")
field = tk.PhotoImage(file="/Users/hw18a153/Desktop/pokemon_mandatory/field.png")

card_ura_image = Image.open("/Users/hw18a153/Desktop/pokemon_mandatory/poke_ura.jpg")
card_ura_image = card_ura_image.resize((90, 125))
card_ura_image = ImageTk.PhotoImage(card_ura_image)


canvas = tk.Canvas(width=950, height=600)
canvas.place(x=0, y=0)
canvas.create_image(0, 0, image=field, anchor=tk.NW, tag="field")

canvas.create_image(727, 143, image=card_ura_image)
# ボタンの作成

btn1 = tk.Button(root, text='スタート',command = btn_click1) # ボタンの設定(text=ボタンに表示するテキスト)
btn1.place(x=700, y=130) #ボタンを配置する位置の設定
create_rectangle(2, 410, 949, 599, fill="green", alpha=0, width=0, tags="hand_place")
create_rectangle(135, 2, 670, 230, fill="blue", alpha=0, width=0, tags="active_place")
create_rectangle(135, 230, 670, 400, fill="green", alpha=0, width=0, tags="bench_Place")
create_rectangle(670, 220, 783, 370, fill="yellow", alpha=.5, width=0, tags="trash")
create_rectangle(670, 70, 783, 220, fill="red", alpha=0, width=0, tags="deck")


canvas.tag_bind("hand_place", "<ButtonPress-1>", place_pressed)
canvas.tag_bind("active_place","<Motion>",active_place_in)
canvas.tag_bind("bench_Place","<Motion>",bench_Place_in)
#canvas.tag_bind("hand_place","<Motion>",card_mouseover)
canvas.tag_bind("trash", "<ButtonPress-1>", trash_check)
#canvas.bind("<Motion>",energie_in_pokemon)
# メインループ
root.mainloop()
		
