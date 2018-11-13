import pickle
fp = open("urls","r")
links = list()
for doc in fp:
	links.append("http://research.baidu.com" + doc[0:len(doc)-1])
file_links = open("links","wb")
pickle.dump(links, file_links)