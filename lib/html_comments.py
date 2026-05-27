import re

html_comment_re_pattern = re.compile(r'[ ]?<!--((?:.|\n)+?)-->')

def strip_html_comments(content_section):
  content_section = html_comment_re_pattern.sub(
      '',
      content_section
    )
  return content_section
