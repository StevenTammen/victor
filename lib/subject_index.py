import re
from .general_utility import read_in_file, safe_open_w, get_link_from_file_path, build_links_for_all_headers, slugify

# -------------------------------------------------------------
# Methods for building subject index map when processing pages

# https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
def store_subject_link(subject_map, keys_in_order_of_access, link_title, link_value):
  # We create dictionaries as many levels deep as we need to.
  # This loop sets the subject_map variable to another nested
  # dictionary each iteration, leaving us ended with the variable
  # referencing the dictionary we want to be assigning the new link in
  for key in keys_in_order_of_access:
    subject_map = subject_map.setdefault(key, {})
  subject_map[link_title] = link_value

def add_single_subject_link_to_subject_map(stag, page_path, study_title, page_title, header_title, subject_map):

  slugified_section_header = slugify(header_title)

  # In case there are missing spaces due to typos
  nested_subject_topics = re.split(r' ?> ?', stag)

  # In case there are extra spaces in there
  nested_subject_topics = [topic.strip() for topic in nested_subject_topics]

  # Escape quotes, so that when this is injected in a Hugo shortcode, quoted headers are supported
  study_title = study_title.replace('"', '\\"')
  page_title = page_title.replace('"', '\\"')
  header_title = header_title.replace('"', '\\"')
  
  subject_index_link_title = f'{study_title} | {page_title} | {header_title}'

  # Only add header id to link path when subject tag is under a header on page, rather than in frontmatter
  subject_index_link_value = f'{get_link_from_file_path(page_path)}/'
  if slugified_section_header != "":
    subject_index_link_value = subject_index_link_value + f'#{slugified_section_header}'

  subject_map = store_subject_link(subject_map, nested_subject_topics, subject_index_link_title, subject_index_link_value)

stags_re_pattern = re.compile(r'stags="(.*)"')
def process_single_properties_stag_list(match_obj, page_path, study_title, page_title, subject_map):
  header_title = match_obj.group(1)
  properties_shortcode_inner = match_obj.group(2)
  match = stags_re_pattern.search(properties_shortcode_inner)
  stags_as_string = match.group(1) if match else None
  if((stags_as_string != None) and (stags_as_string != "")):
    # In case there are missing spaces due to typos
    stags_as_array = re.split(r' ?\| ?', stags_as_string)
    for stag in stags_as_array:
      add_single_subject_link_to_subject_map(stag, page_path, study_title, page_title, header_title, subject_map)

# Make this match headers and new properties shortcode format, to extract 
# replace quotes inside stags="" specification with smart quotes

# Deal with stags in frontmatter that are not inside properties shortcodes
header_and_properties_shortcode_re_pattern = re.compile(r'^#+ (.+) \{\#.+\}\n\n{{< properties((?:.|\n)+?)>}}', re.MULTILINE)
def process_properties_stag_lists_on_page(file_path, file_as_string, study_title, page_title, subject_map):
  for match in header_and_properties_shortcode_re_pattern.finditer(file_as_string):
    process_single_properties_stag_list(match, file_path, study_title, page_title, subject_map)

frontmatter_stag_list_re_pattern = re.compile(r'stags:((?:\s|\n)*-.+)*', re.MULTILINE)
frontmatter_stag_hyphen_list_item_re_pattern = re.compile(r'\s*- (.+)', re.MULTILINE)
def process_frontmatter_stag_list_on_page(file_path, file_as_string, study_title, page_title, subject_map):
  match = frontmatter_stag_list_re_pattern.search(file_as_string)
  stag_hyphen_list = match.group(0) if match else None
  if(stag_hyphen_list):
    for match in frontmatter_stag_hyphen_list_item_re_pattern.finditer(stag_hyphen_list):
      stag = match.group(1) if match else None
      if(stag):
        # header_title = "" since frontmatter subject links do not have page headers associated with them
        add_single_subject_link_to_subject_map(stag, file_path, study_title, page_title, "", subject_map)

# -------------------------------------------------------------
# Methods for turning the subject index map dict into the subject index page itself


def get_content_type_name(link, content_types):
  for path, name in content_types.items():
    if(path in link):
      return name

def get_content_type_slugified(link, content_types):
  for path, name in content_types.items():
    if(path in link):
      if('/' in path):
        return path.split('/')[0]
      else:
        return path

def build_header_on_subject_index_page(topic):
  markdown_header_prefix = '##'
  levels_nested = topic.count('>')
  for i in range(levels_nested):
    markdown_header_prefix = markdown_header_prefix + '#'
  return markdown_header_prefix + ' ' + topic

def add_links_for_topic(output, topic, topic_dict, content_types):
  
  leaf_titles = []
  child_topic_keys = []
  
  for key, value in topic_dict.items():
    if(type(value) is str):
      leaf_titles.append(key)
    else: # type(value) is dict
      child_topic_keys.append(key)
  
  output = output + build_header_on_subject_index_page(topic) + '\n\n'
  
  leaf_titles = sorted(leaf_titles)
  for title in leaf_titles:

    split_title = title.split(" | ")
    study_title = split_title[0]
    page_title = split_title[1]
    header_title = split_title[2]

    link = topic_dict[title]
    content_type_name = get_content_type_name(link, content_types)
    content_type_slugified = get_content_type_slugified(link, content_types)

    # Only add header to subject index link if it is defined
    # Subject links to a page as a whole will not have any header defined
    header_parameter = ""
    if(header_title != ""):
      header_parameter = f'header-title="{header_title}"'

    output = output + f'''{{{{% subject-index-link
content-type="{content_type_name}"
content-type-slugified="{content_type_slugified}"
link="{link}"
study-title="{study_title}"
page-title="{page_title}"
{header_parameter}
%}}}}
\n'''
    
  child_topic_keys = sorted(child_topic_keys)
  for child_topic in child_topic_keys:
    output = output + add_links_for_topic('', topic + ' > ' + child_topic, topic_dict[child_topic], content_types)

  return output

subject_index_replacement_re_pattern = re.compile(r'^<!-- subject-index -->(?:.|\n)+<!-- subject-index -->', re.MULTILINE)
def build_subject_index(subject_map, content_directory, content_types):
  
  output = ''
  topics = sorted(subject_map.keys())
  for topic in topics:
    output = add_links_for_topic(output, topic, subject_map[topic], content_types)

  output = build_links_for_all_headers(output)

  subject_index_path = content_directory + 'meta/' + 'subject-index.md'

  file_content = read_in_file(subject_index_path)
  with safe_open_w(subject_index_path) as f:
    new_file_content = subject_index_replacement_re_pattern.sub(
      f'<!-- subject-index -->\n\n{output}\n\n<!-- subject-index -->',
      file_content
    )
    f.writelines(new_file_content)
