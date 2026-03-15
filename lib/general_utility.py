import markdown
import os, shutil
import re
from slugify import slugify

# https://stackoverflow.com/questions/49640513/
def read_in_file(file_path):
  with open(file_path, "r", encoding="utf8") as f:
    return f.read()

# Clean out everything presently in the /slides directory
def clean_slides_directory(slides_directory):
  for child_path in os.listdir(slides_directory):
      full_path = os.path.join(slides_directory, child_path)
      # Only remove directories. Leave top-level slides alone
      if(os.path.isdir(full_path)):
        shutil.rmtree(full_path)


title_re_pattern = re.compile(r'^title: (.*)\n', re.MULTILINE)
def get_page_title(file_as_string):
  title = title_re_pattern.search(file_as_string).group(1)

  # Sometimes you have to wrap titles in quotes, so that
  # you can use colons. Because YAML otherwise blocks you.
  title = title.strip('"')

  # If you ever have title-internal quotes, you have to escape those in YAML.
  # This properly handles them.
  return title.replace('\"', '"')


weight_re_pattern = re.compile(r'^weight: (.*)\n', re.MULTILINE)
def get_page_weight(file_as_string):
  try:
    return weight_re_pattern.search(file_as_string).group(1)
  # If weight does not exist as a frontmatter variable,
  # transparently return None
  except AttributeError:
    return None



def get_link_from_file_path(file_path):

  # Get the relevant path portion by trimming off everything coming
  # after the content directory (this stuff is the path that gets deployed).
  # See https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring.
  # Want limit of one split, in case the word 'content' shows up in some page title
  link_address = file_path.split("content",1)[1]

  # To keep the code simple, we use the same functions to handle both
  # discussion pages and content pages for each leaf bundle. The simplest way
  # to do this is to make pretend that each content page lives at content-page.md
  # (rather than content-page/_index.md). And then also that each discussion page
  # lives at content-page/discussion-page.md (rather than content-page/discussion-page/index.md)
  link_address = link_address.replace('/_index', '')
  link_address = link_address.replace('/index', '')

  # Remove the '.md' extension
  link_address = link_address[:-3]

  return link_address

def process_aggregation_page_header(match_obj, title):
  header_symbols = match_obj.group(1)
  header_text = match_obj.group(2).strip()

  already_existing_link = match_obj.group(3).strip()
  # remove the {# } from {#link-text-like-this} to leave just link-text-like-this
  already_existing_link_text = already_existing_link[2:-1]

  # We only want to disambiguate via title prepending a single time per link.
  # Discussion page header links will already be disambiguated from when
  # they were initially processed in this method when they were being
  # aggregated the first time on the content page. So they should be ignored
  # when aggregating the content pages themselves onto the aggregation page.
  # This conditional does that ignoring
  slugified_header_text = slugify(header_text)
  # First time disambiguating by prepending title
  # = we do actually need to prepend
  if(already_existing_link_text == slugified_header_text):
    link = ' {#' + slugify(title) + '-' + slugified_header_text + '}'
  # Not first time -- these are discussion page header links 
  # = preserve old link that is already disambiguated
  else: 
    link = ' ' + already_existing_link

  # Nest headers an additional level
  return '#' + header_symbols + header_text + link + '\n'

def process_header(match_obj):
  header_symbols = match_obj.group(1)
  header_text = match_obj.group(2).strip()
  link = ' {#' + slugify(header_text) + '}'
  return header_symbols + header_text + link + '\n'

def strip_link_part_of_header(match_obj):
  header_symbols = match_obj.group(1)
  header_text = match_obj.group(2).strip()
  return header_symbols + header_text + '\n'

header_re_pattern = re.compile(r'^(#+ )([^{\n]+)(.*)\n', re.MULTILINE)
def build_links_for_all_headers(file_as_string):
  # Manually build ids for headers with Python's slugify package, to match links between pages and subject index.
  # Hugo supports building these header ids automatically normally, but then the header ids wouldn't match the
  # any links constructed with the Python library, hence *all* of them must be built with the Python package
  new_file_content = header_re_pattern.sub(
      lambda match: process_header(match),
      file_as_string
  )
  return new_file_content


def initial_full_content_processing(full_content_for_aggregation, title, file_path, discussion_pages_section):

  # Remove section navigation shortcodes, since don't need section navigation on the
  # aggregation page
  full_content_for_aggregation = full_content_for_aggregation.replace("{{% section-navigation %}}", "")

  # Make content sections and transcript sections toggleable on aggregation pages, as well as discussion page sections
  full_content_for_aggregation = full_content_for_aggregation.replace("{{% content %}}", "{{% toggleable-content %}}")
  full_content_for_aggregation = full_content_for_aggregation.replace("{{% /content %}}", "{{% /toggleable-content %}}")
  full_content_for_aggregation = full_content_for_aggregation.replace("{{% transcript %}}", "{{% toggleable-transcript %}}")
  full_content_for_aggregation = full_content_for_aggregation.replace("{{% /transcript %}}", "{{% /toggleable-transcript %}}")

  if(discussion_pages_section != ''):
    full_content_for_aggregation = full_content_for_aggregation.replace("{{% discussion-pages %}}", "{{% toggleable-discussion-pages %}}")
    full_content_for_aggregation = full_content_for_aggregation.replace("{{% /discussion-pages %}}", "{{% /toggleable-discussion-pages %}}")

  # Manually build links for headers (Hugo doesn't de-duplicate headers in
  # shortcodes)
  full_content_for_aggregation = header_re_pattern.sub(
    lambda match: process_aggregation_page_header(match, title),
    full_content_for_aggregation
  )

  # Create a link to the leaf page. The text will be the page's title, and the link
  # address will point to the page's path relative to the site's root. (Hence working
  # both when running on the local webserver on localhost, and when deployed).

  link_address = get_link_from_file_path(file_path)

  # Build link from title and link address. We also need to add the slugified id here, otherwise hugo tries to
  # automatically build an id for the header based on the anchor tag and it gets all messed up.
  header_id = '{#' + slugify(title) + '}'
  link = f'[{title}]({link_address}) {header_id}'

  # Add h2 title of the page, so everything displays properly on aggregate page
  # The incoming full_content_for_aggregation already starts with two newline characters
  full_content_for_aggregation = f"\n\n## {link}" + full_content_for_aggregation

  return full_content_for_aggregation

commented_out_slide_break_re_pattern = re.compile(r'<!-- --- -->')
# https://blog.finxter.com/python-regex-start-of-line-and-end-of-line/
h2_header_re_pattern = re.compile(r'^## (.+)', re.MULTILINE)
def initial_content_section_processing(content_section, title):

  # First uncomment the slide breaks so that they will be active
  content_section = commented_out_slide_break_re_pattern.sub('\n\n---\n\n', content_section)

  # Remove the header saying that this section is the the content.
  # At this point, it will be the only h2 header in the full-text string
  content_section = h2_header_re_pattern.sub('', content_section)

  # Don't have {#header-ids} for headers in slides
  content_section = header_re_pattern.sub(
    lambda match: strip_link_part_of_header(match),
    content_section
  )

  # Add actual page title to the content section, so that the title shows up in the slides.
  content_section = f'## {title}{content_section}'

  return content_section

# https://stackoverflow.com/questions/49640513/
def read_in_file(file_path):
  with open(file_path, "r", encoding="utf8") as f:
    return f.read()

def convert_text_to_html(text):
  return markdown.markdown(text)

def safe_open_w(path):
  '''
  Open "path" for writing, creating any parent directories as needed.

  https://stackoverflow.com/a/23794010
  '''
  os.makedirs(os.path.dirname(path), exist_ok=True)
  return open(path, 'w', encoding="utf8")

def build_slides(file_path, template, content_section):
  
  # Replace any back slashes in path with forward slashes
  file_path = file_path.replace('\\', '/')  
  
  output_file_path = file_path.replace('content', 'content/slides')


  #output_file_path = output_file_path.replace('/index', '')
  output_file_path = output_file_path.replace('/_index', '/index')

  output_file_path = output_file_path.replace('.md', '.html')
  to_write = re.sub('markdown-content', content_section, template)
  with safe_open_w(output_file_path) as f:
    f.writelines(to_write)

aggregate_page_replacement_re_pattern = re.compile(r'^<!-- aggregate-page-content -->(?:.|\n)+<!-- aggregate-page-content -->', re.MULTILINE)
def build_aggregation_page(aggregate_page_path, existing_aggregate_page_content, new_aggregate_page_content):
  with safe_open_w(aggregate_page_path) as f:
    new_file_content = aggregate_page_replacement_re_pattern.sub(
      f'<!-- aggregate-page-content -->{new_aggregate_page_content}<!-- aggregate-page-content -->',
      existing_aggregate_page_content
    )
    f.writelines(new_file_content)
  