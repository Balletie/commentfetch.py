from __future__ import print_function
import praw
import textwrap
import types
from HTMLParser import HTMLParser

ts1 = '1310632807' # 7/4/2011
ts2 = '1388023200' # 12/26/2013
last_50 = deque(maxlen=50)
user_name = 'michael_dorfman'
subreddit_name = 'Buddhism'
more_comments = praw.objects.MoreComments
wrapper = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
h = HTMLParser()

def query_str(ts1, ts2):
	return 'timestamp:' + ts1 + '..' + ts2

def print_comment_term(comment, level):
	if isinstance(comment.author, types.NoneType):
		author = "[deleted]"
	else:
		author = comment.author.name
	print(' |  '*level,'Username: ',author,', Score: ',`comment.score`,sep='')
	print(' |  '*level,'Permalink: '+comment.permalink,sep='')
	wrapper.initial_indent=' |  '*level + "Text:   "
	wrapper.subsequent_indent=' |  '*(level + 2)
	print(wrapper.fill(h.unescape(comment.body)).encode('ascii','ignore'))
	print(wrapper.fill(comment.body.encode('ascii','ignore')))
	print(' |  '*(level + 1))

def print_comment(comment, level):
	if isinstance(comment.author, types.NoneType):
		author = "[deleted]"
	else:
		author = comment.author.name
	print('<pre>', 'Username: ',author,', Score: ',`comment.score`,sep='')
	print('Permalink: <a href=\"',
	      comment.permalink.encode('ascii','ignore'),
	      '\">Link</a>',
	      ', Thread link: <a href=\"',
	      comment.submission.short_link,
	      '\">',
	      comment.submission.title.encode('ascii','ignore'),
	      '</a>',
	      ', <a href=\"#\" onclick=\"return hide(this);\">[-]</a>' if level==0 else "",
	      '</pre>',sep='')
	print(h.unescape(comment.body_html.encode('ascii','ignore')))	

def print_tree(commentTree, level, maxlevel=None):
	if maxlevel == None:
		maxlevel=10
	if level == maxlevel:
		return
	print('<div class=\"allnested\">')
	for comment in commentTree:
		print('<div class=\"nested\">')
		print_comment(comment,level)
		print_tree(comment.replies, level + 1, maxlevel)
		print('</div>')
	print('</div>')

r = praw.Reddit('commentfetcher by Skipperr')
r.login(username='uname', password='pswd')

print('<html><head>',
      '<link href=\"stylesheet.css\" rel=\"stylesheet\" type=\"text/css\"/>',
      '<script src=\"showhide.js\"></script>',
      '</head><body><a onclick=\"return hideAll()\" href=\"#\">Hide All</a><div>')
while True:
	last_created = None
	try: 
		results_gen = r.search(query_str(ts1, ts2),
				subreddit=subreddit_name,
				sort='new',
				syntax='cloudsearch', 
				limit=None)
	except HTTPError, e:
		print 'Search from {0} to {1} produced error: {2}'.format(ts1, ts2, e.code)
		sleep(60)
		continue
	for submission in results_gen:
		if submission.id in last_50:
			continue
		last_50.append(submission.id)
		last_created = str(trunc(submission.created_utc) + offset)
		m_comments = submission.comments
		for comment in m_comments:
			if comment.parent_id == comment.link_id:
				print('<div class=\"root\">')
				print_comment(comment, 0)
				print_tree(comment.replies, 1)
				print('</div>')

	if not last_created:
		break
	ts2 = last_created
print('</div></body></html>')
