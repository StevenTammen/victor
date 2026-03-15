import os

from .general_utility import *
from .duplicate_headers import *
from .footnotes import *
from .html_comments import *
from .outlines import *
from .special_content_sections import *
from .other_shortcodes import *
from .step_bible_iframes import *
from .subject_index import *

class Study:
  def __init__(self, aggregation_page_path, content_pages):
    self.aggregation_page_path = aggregation_page_path
    self.content_pages = content_pages

def study_has_multiple_lessons(study_path):
  subdirectory_paths = [ f.path for f in os.scandir(study_path) if f.is_dir() ]
  # If there are no subdirectories, it must be the case that the study only has 
  # a single lesson, having its content in study_path/_index.md
  if(len(subdirectory_paths) == 0):
    return False
  # If there is at least one subdirectory, then we have to check to see whether
  # the subdirectories contain index.md files or _index.md files. (We could also
  # check if these subdirectories in turn had subdirectories of their own). What we
  # are checking is if the Hugo bundles are branch bundles or leaf bundles.
  # (See https://gohugo.io/content-management/page-bundles/).
  # We can get away only checking the first one, since all subdirectories 
  # directly under the study directory will behave the same = either all be for 
  # lesson pages or all be for discussion pages, one or the other.
  else:
    files_in_first_subdirectory = [ f.name for f in os.scandir(subdirectory_paths[0]) ]
    if('_index.md' in files_in_first_subdirectory):
      return True
    else:
      return False

# If you ever want to check for content in pages that are directly in content/:
# https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
def build_list_of_content_groups_to_process(content_directory, content_type_paths):
  base_path = content_directory
  studies = []
  for relative_content_type_path in content_type_paths:
    full_content_type_path = base_path + relative_content_type_path
    # https://stackoverflow.com/a/40347279
    study_paths = [ f.path for f in os.scandir(full_content_type_path) if f.is_dir() ]
    for study_path in study_paths:
      # Study has multiple lessons
      if(study_has_multiple_lessons(study_path)):
        aggregation_page_path = os.path.join(study_path, "_index.md")
        content_pages = {}
        lesson_paths = [ f.path for f in os.scandir(study_path) if f.is_dir() ]
        for lesson_path in lesson_paths:
          content_page_path = os.path.join(lesson_path, "_index.md")
          discussion_page_paths = [ os.path.join(f.path, "index.md") for f in os.scandir(lesson_path) if (f.is_dir() and not ('recording' in f.name)) ]
          content_pages[content_page_path] = discussion_page_paths
        study = Study(aggregation_page_path, content_pages)
        studies.append(study)
      # Study only has a single lesson (even though that lesson might still 
      # contain multiple discussion pages). No aggregation page in this instance.
      else:
        aggregation_page_path = ''
        content_pages = {}
        content_page_path = os.path.join(study_path, "_index.md")
        discussion_page_paths = [  os.path.join(f.path, "index.md") for f in os.scandir(study_path) if f.is_dir() ]
        content_pages[content_page_path] = discussion_page_paths
        study = Study(aggregation_page_path, content_pages)
        studies.append(study)
  return studies

discussion_pages_section_replacement_re_pattern = re.compile(r'^{{% discussion-pages %}}(?:.|\n)+{{% /discussion-pages %}}', re.MULTILINE)
def process_leaf_page(file_path, study_title, subject_map, discussion_pages_section):

  # Replace any back slashes in path with forward slashes
  file_path = file_path.replace('\\', '/')

  file_as_string = read_in_file(file_path)

  page_title = get_page_title(file_as_string)
  page_weight = get_page_weight(file_as_string)
  new_file_content = build_subjects_sections_on_page(file_path, file_as_string, study_title, page_title, subject_map)
  
  if(discussion_pages_section != ''):
    # f-strings in python get weird with {}. Why we use + concatenation operator
    new_file_content = discussion_pages_section_replacement_re_pattern.sub(
      "{{% discussion-pages %}}" + discussion_pages_section + "{{% /discussion-pages %}}",
      new_file_content
    )

  # Ensure all subjects in subjects sections are overwritten with the proper hyperlink format
  with safe_open_w(file_path) as f:
    f.writelines(new_file_content)

  page = get_page_info(file_path, new_file_content, page_title, page_weight, discussion_pages_section)

  return page


class Page:
  def __init__(self, title, weight, full_content_for_aggregation, summary, content_section_for_slides):
    self.title = title
    self.weight = weight
    self.full_content_for_aggregation = full_content_for_aggregation
    self.summary = summary
    self.content_section_for_slides = content_section_for_slides

everything_but_frontmatter_re_pattern = re.compile(r'^---(?:.|\n)+?---\n((?:.|\n)+)', re.MULTILINE)
# This regular expression just gets the first content section --
# the one for the content page, not all the content sections of 
# any discussion pages associatd with the content page
content_section_re_pattern = re.compile(r'^{{% content %}}((?:.|\n)+?){{% /content %}}', re.MULTILINE)
summary_re_pattern = re.compile(r'^## Summary.*\n\n((?:.|\n)+?)(?=\n#)', re.MULTILINE)
def get_page_info(file_path, file_as_string, title, weight, discussion_pages_section):

  full_content_for_aggregation = everything_but_frontmatter_re_pattern.search(file_as_string).group(1)
  
  # Only populate summary field if it exists
  summary = summary_re_pattern.search(full_content_for_aggregation)
  if(summary != None):
    summary = summary.group(1)

  content_section_for_slides = content_section_re_pattern.search(full_content_for_aggregation)
  if(content_section_for_slides != None):
    content_section_for_slides = content_section_for_slides.group(1)
    content_section_for_slides = initial_content_section_processing(content_section_for_slides, title)

  full_content_for_aggregation = initial_full_content_processing(full_content_for_aggregation, title, file_path, discussion_pages_section)

  page = Page(
    title,
    weight,
    full_content_for_aggregation,
    summary,
    content_section_for_slides
  )

  return page

discussion_pages_re_pattern = re.compile(r'^{{% discussion-pages %}}((?:.|\n)+?){{% /discussion-pages %}}', re.MULTILINE)
def strip_discussion_pages(content_section):
  content_section = discussion_pages_re_pattern.sub(
      '',
      content_section
    )
  return content_section

video_only_sections_re_pattern = re.compile(r'^{{% video-only %}}((?:.|\n)+?){{% /video-only %}}', re.MULTILINE)
def strip_video_only_sections(content_section):
  content_section = video_only_sections_re_pattern.sub(
      '',
      content_section
    )
  return content_section

slides_template = read_in_file('templates/slides-template.html')
def process_content_section_and_build_slides(file_path, content_section, summary):

    # Strip discussion pages, video-only sections, html comments, and subjects sections
    content_section = strip_discussion_pages(content_section)
    content_section = strip_video_only_sections(content_section)
    content_section = strip_html_comments(content_section)
    content_section = strip_subjects_sections(content_section)

    # Add duplicate headers to slides, as necessary
    content_section = add_duplicate_headers_as_necessary(content_section)

    # Preprocess footnotes into littlefoot-ready HTML
    content_section = parse_footnotes(content_section)

    # Add outline
    content_section = add_appropriate_things_to_beginning_and_end_of_slides(content_section, summary)

    # Convert shortcodes to STEP Bible iframes
    content_section = replace_nt_step_bible_shortcodes(content_section)
    content_section = replace_ot_step_bible_shortcodes(content_section)

    # Replace properties shortcode with embedded video/audio HTML
    content_section = replace_properties_shortcodes(content_section)

    # Replace special content sections
    content_section = replace_special_content_sections(content_section)
    content_section = render_markdown_and_split_across_slides(content_section)

    # Write slides to output file
    build_slides(file_path, slides_template, content_section)