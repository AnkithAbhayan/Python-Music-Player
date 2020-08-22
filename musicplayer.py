import os
import json
import pygame
import random
import time
from pathlib import Path
from tkinter import filedialog
from tkinter import *
root = Tk()
pygame.mixer.init()
def sort(data):
    new_list = []
    alpha = []
    integers = []
    characters = []
    alphabets = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    numbers = [0,1,2,3,4,5,6,7,8,9]
    for item in data:
        if str(item)[0].lower() in alphabets:
            alpha.append(item)
        elif str(item)[0] in numbers:
            integers.append(item)
        else:
            characters.append(item)
    dict1 = {}
    for item in alpha:
        if str(item)[0].islower():
            unix = []
            not_upper = item
            for letter in item:
                unix.append(letter)
            unix[0] = unix[0].upper()
            is_upper = ""
            for letter in unix:
                is_upper += letter
            index = alpha.index(item)
            del alpha[index]
            alpha.insert(index,is_upper)
            dict1.update({is_upper:not_upper})
    alpha.sort()
    for item in alpha:
        try:
            item1 = dict1[item]
            index = alpha.index(item)
            alpha[index] = item1
        except KeyError:
            pass
    integers.sort()
    integers.extend(alpha)
    alpha.clear()
    characters.sort()
    characters.extend(integers)
    return characters
def make_json_file():
    data11={}
    with open("trial_file.json", "w") as jsonFile:
        json.dump(data11,jsonFile,indent=4)
    with open("trial_file.json", "r") as jsonFile:
        data = json.load(jsonFile)      
    make_new_stuff(data)
def check_if_there_is_songs_added():
    jsonFile = "trial_file.json"
    exists = os.path.exists(jsonFile)
    if exists == True:
        if os.path.getsize(jsonFile) > 3:
            pass            
        else:
            make_json_file()
    else:
        make_json_file()
def make_new_stuff(data):
    datas = {
        "song_paths":[
            {
        "path":"",
        "songs_in_path":[],
        "number_of_songs":"",
        }
        ],
        "current_sort":"",
        "current_song":"",
        "all_possible_sorts":["by_path","date_added_ascending","date_added_descending","alphabetical_ascending","alphabetical_descending","size_ascending","size_descending","random_shuffle"],
        "current_song_list":[],
        "current_song_list_path":[]
        }
    path = filedialog.askdirectory()
    datas["song_paths"][0]["path"] = path
    with open("trial_file.json", "w") as jsonFile:
        json.dump(datas,jsonFile,indent=4)
def refresh(): 
    with open("trial_file.json", "r") as jsonFile:
        data = json.load(jsonFile)  
    todo = True
    data["current_song_list"].clear()
    data["current_song_list_path"].clear()
    current_song_list = []
    current_song_list_path = []
    for i in range(len(data["song_paths"])):
        path = data["song_paths"][i]["path"]
        exists = os.path.exists(path)
        if exists == False:
            del data["song_paths"][i]
        else:
            for item in data["song_paths"][i]["songs_in_path"]:
                song_name = data["song_paths"][i]["path"]+"/"+item
                if os.path.exists(path):
                    pass
                else:
                    index = data["song_paths"][i]["songs_in_path"].index(item)
                    del data["song_paths"][i]["songs_in_path"][index]
    for i in range(len(data["song_paths"])):
        is_upper = []
        path = data["song_paths"][-i]["path"]
        song_names = os.listdir(data["song_paths"][-i]["path"])
        matrix = []
        for item in song_names:
            matrix.append(path+"/"+item)
        matrix.sort(key=os.path.getmtime)
        length = len(path)
        newtrix = []
        for item in matrix:
            newtrix.append(item[length+1:len(item)+1])
        newtrix.reverse()
        data["song_paths"][-i]["songs_in_path"].clear()
        data["song_paths"][-i]["songs_in_path"].extend(newtrix)
        data["number_of_songs"] = len(newtrix)
        for item in newtrix:
            current_song_list_path.append(path+"/"+item)
    sort1 = data["current_sort"]
    print(sort1+"aaaa")
    if sort1 == "by path":
        pass
    elif sort1 == "date_added_ascending":
        current_song_list_path.sort(key=os.path.getmtime)
    elif sort1 == "date_added_descending":
        current_song_list_path.sort(key=os.path.getmtime)
        current_song_list_path.reverse()
    elif sort1 == "size_ascending":
        current_song_list_path.sort(key=os.path.getsize)
    elif sort1 == "size_descending":
        current_song_list_path.sort(key=os.path.getsize)
        current_song_list_path.reverse()
    elif sort1 == "alphabetical_ascending":
        todo = False
        dict1 = {}
        current_song_list_path_oh = []
        for path in current_song_list_path:
            letters = []
            indexes = []
            for letter in path:
                letters.append(letter)
            for item in letters:
                if item == "/":
                    point = letters.index(item)
                    indexes.append(point)
                    letters[point] = "a"
            point1 = indexes[-1]
            point2 = len(str(path))
            song_name = path[point1+1:point2]
            path = path[0:point1]
            current_song_list.append(song_name)
            current_song_list_path_oh.append(path+"/")
            letters.clear()
            indexes.clear()
        current_song_list_path.clear()
        current_song_list_path.extend(current_song_list_path_oh)
        current_song_list_path_oh.clear()
        for i in range(len(current_song_list_path)):
            dict1.update({current_song_list[i]:current_song_list_path[i]})
        current_song_list = sort(current_song_list)
        new_array = []
        for item in current_song_list:
            full_name = ""
            path = dict1[item]
            full_name+=path
            full_name+=item
            new_array.append(full_name)
        current_song_list_path.clear()
        current_song_list_path.extend(new_array)
        data["current_song_list"] = current_song_list
        data["current_song_list_path"] = current_song_list_path
    elif sort1 == "alphabetical_descending":
        todo = False
        dict1 = {}
        current_song_list_path_oh = []
        for path in current_song_list_path:
            letters = []
            indexes = []
            for letter in path:
                letters.append(letter)
            for item in letters:
                if item == "/":
                    point = letters.index(item)
                    indexes.append(point)
                    letters[point] = "a"
            point1 = indexes[-1]
            point2 = len(str(path))
            song_name = path[point1+1:point2]
            path = path[0:point1]
            current_song_list.append(song_name)
            current_song_list_path_oh.append(path+"/")
            letters.clear()
            indexes.clear()
        current_song_list_path.clear()
        current_song_list_path.extend(current_song_list_path_oh)
        current_song_list_path_oh.clear()
        for i in range(len(current_song_list_path)):
            dict1.update({current_song_list[i]:current_song_list_path[i]})
        current_song_list = sort(current_song_list)
        new_array = []
        for item in current_song_list:
            full_name = ""
            path = dict1[item]
            full_name+=path
            full_name+=item
            new_array.append(full_name)
        current_song_list_path.clear()
        current_song_list_path.extend(new_array)
        new_array.clear()
        current_song_list.reverse()
        current_song_list_path.reverse()
        data["current_song_list"] = current_song_list
        data["current_song_list_path"] = current_song_list_path

    elif sort1 == "random_shuffle":
        random.shuffle(current_song_list_path)
    if todo == True:
        for path in current_song_list_path:
            letters = []
            indexes = []
            for letter in path:
                letters.append(letter)
            for item in letters:
                if item == "/":
                    point = letters.index(item)
                    indexes.append(point)
                    letters[point] = "a"
            point1 = indexes[-1]
            point2 = len(str(path))
            song_name = path[point1+1:point2]
            current_song_list.append(song_name)
            letters.clear()
            indexes.clear()
        data["current_song_list"] = current_song_list
        data["current_song_list_path"] = current_song_list_path
    for item in data['current_song_list']:
        print(item)
    with open("trial_file.json","w") as jsonFile:
        json.dump(data,jsonFile,indent=4)
def add_new_path(data):
    path1 = filedialog.askdirectory()
    if path1 == '':
        pass
    else:
        song_names = os.listdir(path1)
        new_file = {
        "path":"",
        "songs_in_path":[],
        "number_of_songs":"",
        }
        data["song_paths"].append(new_file)
        length = len(data["song_paths"])
        data["song_paths"][-1]["path"] = path1
        with open("trial_file.json","w") as jsonFile:
            json.dump(data,jsonFile,indent=4)
def change_sort(sorter,sort):
    with open("trial_file.json", "r") as jsonFile:
        data = json.load(jsonFile)    
    data['current_sort'] = sort
    with open("trial_file.json","w") as jsonFile:
        json.dump(data,jsonFile,indent=4)    
    sorter.destroy()
def choose_sort():
    with open("trial_file.json","r") as jsonFile:
        data = json.load(jsonFile)    
    data['current_sort'] = ""
    with open("trial_file.json","w") as jsonFile:
        json.dump(data,jsonFile,indent=4)
    sorter = Tk()
    message = Label(sorter,text="what kind of sorting would you like to implement to your song list?").grid(row=0,column=0) 
    button_bypath = Button(sorter,width=40,text="by path",command=lambda:change_sort(sorter,"by_path")).grid(row=1,column=0)
    button_date_added_ascending = Button(sorter,width=40,text="date added(oldest first)",command=lambda:change_sort(sorter,"date_added_ascending")).grid(row=2,column=0)
    button_date_added_descending = Button(sorter,width=40,text="date added(newest first)",command=lambda:change_sort(sorter,"date_added_descending")).grid(row=3,column=0)
    button_size_ascending = Button(sorter,width=40,text="size ascending",command=lambda:change_sort(sorter,"size_ascending")).grid(row=4,column=0)
    button_size_descending = Button(sorter,width=40,text="size descending",command=lambda:change_sort(sorter,"size_descending")).grid(row=5,column=0)
    button_alphabetical_ascending = Button(sorter,width=40,text="alphabetical order(A-Z)",command=lambda:change_sort(sorter,"alphabetical_ascending")).grid(row=6,column=0)
    button_alphabetical_descending = Button(sorter,width=40,text="alphabetical order(Z-A)",command=lambda:change_sort(sorter,"alphabetical_descending")).grid(row=7,column=0)
    button_random_shuffle = Button(sorter,width=40,text="random",command=lambda:change_sort(sorter,"random_shuffle")).grid(row=8,column=0)
    sorter.mainloop()
def add_path():
    with open("trial_file.json","r") as jsonFile:
        data = json.load(jsonFile)
    add_new_path(data)
def destroy():
    root.destroy()
def new_path(data):
    for i in range(len(data['song_paths'])):
        all_paths = Label(root,text=data["song_paths"][i]["path"]).grid(row=i,column=0)
    newpath = Label(root,text="enter new path?").grid(row=len(data['song_paths']),column=0,columnspan=2)
    yes = Button(root,text="yes",width=10,command=add_path).grid(row=len(data['song_paths'])+1,column=0)
    no = Button(root,text="no",width=10,command=destroy).grid(row=len(data['song_paths'])+1,column=1)
    root.mainloop()
def play_songs():
    check_if_there_is_songs_added()
    with open("trial_file.json", "r") as jsonFile:
        data = json.load(jsonFile)   
    refresh()   
    new_path(data)
    choose_sort()
    refresh()
    with open("trial_file.json", "r") as jsonFile:
        data = json.load(jsonFile) 
    for item in data["current_song_list_path"]:
        index = data["current_song_list_path"].index(item)
        print(data["current_song_list"][index])
        pygame.mixer.music.load(item)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        time.sleep(2)
play_songs()