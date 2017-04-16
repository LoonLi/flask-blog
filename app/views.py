from flask import render_template,render_template_string
from os import listdir
from os.path import isfile, join
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from app import app
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        try:
        	lexer = get_lexer_by_name(lang, stripall=True)
        	formatter = html.HtmlFormatter()        	
        	text = highlight(code, lexer, formatter)
        except Exception as e:
        	text = '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        return text

class mdParser(object):
	"""Get info and text from md"""
	def __init__(self, md_file):
		self.info = self.getInfo(md_file)
		self.text = md_file.read()
		text = self.text
		first_line = text[:self.text.find('\n')]
		self.info['first_line'] = first_line
		
	def getTitle(self,line):
		line = line[line.find(':')+1:-1]
		line = line.replace(' ','')
		line = line.replace('"','')
		return line[:]

	def getDate(self,line):
		frag = line.split(' ')
		frag = [i for i in frag if i != '']
		ymd = frag[1].split('-')
		time_dic = {}
		time_dic['year'] = ymd[0]
		time_dic['month'] = ymd[1]
		time_dic['day'] = ymd[2]
		return time_dic

	def getCategories(self,line):
		categ = line[line.find(':')+1:-1]
		categ = categ.split(',') 
		return [i.replace(' ','') for i in categ]

	def getPub(self,line):
		return 'true' in line

	def getInfo(self,f):
		file_line = []
		for i in range(7):
			file_line.append(f.readline())
		title = self.getTitle(file_line[2])
		date = self.getDate(file_line[3])
		categ = self.getCategories(file_line[4])
		pub = self.getPub(file_line[5])
		info_dic = {}
		info_dic['title'] = title
		info_dic['date'] = date
		info_dic['categories'] = categ
		info_dic['published'] = pub
		return info_dic

class dirParser(object):
	"""Get all markdowns and their infomation from a dir."""
	def __init__(self, path):
		self.file_list = self.getMds(path)
		self.pages = (len(self.file_list)/10)+1

	def getFiles(self,path):
		return [ f for f in listdir(path) if isfile(join(path,f)) ]

	def getMds(self,path):
		md_list = []
		ff = self.getFiles(path)
		for f in ff:
			md_list.append(mdParser(open(path+"/"+f)))
			md_list[-1].info['file_name'] = f
		return md_list


base_path = "/root/flask-blog/app/"

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
	mds = dirParser(base_path+"/static/posts")
	posts = []
	for md in mds.file_list:
		posts.append(md.info)
	pages = {}
	if page < 1:
		page = 1
	if page > mds.pages:
		page = mds.pages
	if mds.pages > 5 and page > 4:
		if (page+2)>mds.pages:
			result = range(mds.pages-4,mds.pages+1)
		else:
			result = [x for x in range(mds.pages) if x > page-3 or x < page+3]
	else:
		result = range(1,mds.pages+1)
	pages['count'] = result
	pages['pre'] = page-1
	pages['next'] = page+1
	pages['page'] = page
	posts = posts[::-1]
	posts = posts[10*(page-1):10*page]
	return render_template("index.html",posts=posts,pages=pages)

@app.route('/post/<file_name>')
def post(file_name):
	md = mdParser(open(base_path+"/static/posts/"+file_name))
	renderer = HighlightRenderer()
	markdown = mistune.Markdown(renderer=renderer)
	text = markdown(md.text)
	return render_template("post.html", post=md.info, text=text)

@app.route('/about')
def about():
	return render_template("about.html")