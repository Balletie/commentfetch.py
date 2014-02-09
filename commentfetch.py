from __future__ import print_function
import praw
import textwrap
import types
from HTMLParser import HTMLParser
	
wrapper = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
h = HTMLParser()

def printCommentTerm(comment, level):
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

def printComment(comment, level):
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
	      comment.submission.title,
	      '</a>'
	      '</pre>',sep='')
	print(h.unescape(comment.body_html.encode('ascii','ignore')))	

def printTree(commentTree, level, maxlevel=None):
	if maxlevel == None:
		maxlevel=10
	if level == maxlevel:
		return
	for comment in commentTree:
		print('<div class=\"nested\">')
		printComment(comment,level)
		printTree(comment.replies, level + 1, maxlevel)
		print('</div>')

r = praw.Reddit('commentfetcher by Skipperr')
#submission = r.get_submission(submission_id='1xcy87')
#comments = submission.comments
#printTree(comments, 0, 4)

redditor = r.get_redditor("michael_dorfman")
m_comments = redditor.get_comments(limit=None)
print('<html><head><link href=\"test.css\" rel=\"stylesheet\" type=\"text/css\"/></head><body>')
for comment in m_comments:
	if comment.parent_id == comment.link_id:
		print('<div class=\"root\">')
		printComment(comment, 0)
		printTree(comment.replies, 1, 6)
		print('</div>')
print('</body></html>')
