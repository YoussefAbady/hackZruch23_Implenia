
file_path = "C:/Users/yyahiya/Desktop/cur.txt"
new_file = "C:/Users/yyahiya/Desktop/cur_up.txt"

f = open(file_path, "r",encoding='UTF-8')
f_n = open(new_file, "w",encoding='UTF-8')
Lines = f.readlines()

for line in Lines:
  words = line.split(',')
  words.insert(0,words[0].replace(' ','_'))
  words.remove(words[words.__len__()-1])
  words[words.__len__()-1]= words[words.__len__()-1]+'\n'
  f_n.write(','.join(words))


