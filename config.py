class Project:
  def __init__(self, title, project_path, content_types):
    self.title = title
    self.project_path = project_path
    self.content_types = content_types

# ---------------- Change things here ----------------

# Define projects that the preprocessor can be run on
# Make sure you include a trailing slash for the project path.

example = Project(
  "Example",
  "example-site/",
  {
    'sources' : 'Sources'
  }
)

bibledocs = Project(
  "BibleDocs.org",
  "C:/R/bibledocs.org/",
  {
    'shorter-topical-studies' : 'Shorter Topical',

    'longer-topical-studies' : 'Longer Topical',

    'questions-and-answers/self-generated' : 'Self-gen Q&A',
    'questions-and-answers/reader-correspondence' : 'Reader Q&A',

    'verse-by-verse-studies/genesis' : 'Genesis',
    # 'verse-by-verse-studies/exodus' : 'Exodus',
    # 'verse-by-verse-studies/leviticus' : 'Leviticus',
    # 'verse-by-verse-studies/numbers' : 'Numbers',
    # 'verse-by-verse-studies/deuteronomy' : 'Deuteronomy',
    # 'verse-by-verse-studies/joshua' : 'Joshua',
    # 'verse-by-verse-studies/judges' : 'Judges',
    # 'verse-by-verse-studies/ruth' : 'Ruth',
    # 'verse-by-verse-studies/1-samuel' : '1 Sam.',
    # 'verse-by-verse-studies/2-samuel' : '2 Sam.',
    # 'verse-by-verse-studies/1-kings' : '1 Kings',
    # 'verse-by-verse-studies/2-kings' : '2 Kings',
    # 'verse-by-verse-studies/1-chronicles' : '1 Chron.',
    # 'verse-by-verse-studies/2-chronicles' : '2 Chron.',
    # 'verse-by-verse-studies/ezra' : 'Ezra',
    # 'verse-by-verse-studies/nehemiah' : 'Nehemiah',
    # 'verse-by-verse-studies/esther' : 'Esther',
    # 'verse-by-verse-studies/job' : 'Job',
    # 'verse-by-verse-studies/psalms' : 'Psalms',
    # 'verse-by-verse-studies/proverbs' : 'Proverbs',
    # 'verse-by-verse-studies/ecclesiastes' : 'Ecclesiastes',
    # 'verse-by-verse-studies/song-of-solomon' : 'Song of Sol.',
    # 'verse-by-verse-studies/isaiah' : 'Isaiah',
    # 'verse-by-verse-studies/jeremiah' : 'Jeremiah',
    # 'verse-by-verse-studies/lamentations' : 'Lamentations',
    # 'verse-by-verse-studies/ezekiel' : 'Ezekiel',
    # 'verse-by-verse-studies/daniel' : 'Daniel',
    # 'verse-by-verse-studies/hosea' : 'Hosea',
    # 'verse-by-verse-studies/joel' : 'Joel',
    # 'verse-by-verse-studies/amos' : 'Amos',
    # 'verse-by-verse-studies/obadiah' : 'Obadiah',
    # 'verse-by-verse-studies/jonah' : 'Jonah',
    # 'verse-by-verse-studies/micah' : 'Micah',
    # 'verse-by-verse-studies/nahum' : 'Nahum',
    # 'verse-by-verse-studies/habakkuk' : 'Habakkuk',
    # 'verse-by-verse-studies/zephaniah' : 'Zephaniah',
    # 'verse-by-verse-studies/haggai' : 'Haggai',
    # 'verse-by-verse-studies/zechariah' : 'Zechariah',
    # 'verse-by-verse-studies/malachi' : 'Malachi',
    # 'verse-by-verse-studies/matthew' : 'Matthew',
    # 'verse-by-verse-studies/mark' : 'Mark',
    # 'verse-by-verse-studies/luke' : 'Luke',
    # 'verse-by-verse-studies/john' : 'John',
    # 'verse-by-verse-studies/acts' : 'Acts',
    'verse-by-verse-studies/romans' : 'Romans',
    # 'verse-by-verse-studies/1-corinthians' : '1 Cor.',
    # 'verse-by-verse-studies/2-corinthians' : '2 Cor.',
    # 'verse-by-verse-studies/galatians' : 'Galatians',
    # 'verse-by-verse-studies/ephesians' : 'Ephesians',
    # 'verse-by-verse-studies/philippians' : 'Philippians',
    # 'verse-by-verse-studies/colossians' : 'Colossians',
    'verse-by-verse-studies/1-thessalonians' : '1 Thess.',
    # 'verse-by-verse-studies/2-thessalonians' : '2 Thess.',
    # 'verse-by-verse-studies/1-timothy' : '1 Tim.',
    # 'verse-by-verse-studies/2-timothy' : '2 Tim.',
    # 'verse-by-verse-studies/titus' : 'Titus',
    # 'verse-by-verse-studies/philemon' : 'Philemon',
    # 'verse-by-verse-studies/hebrews' : 'Hebrews',
    # 'verse-by-verse-studies/james' : 'James',
    # 'verse-by-verse-studies/1-peter' : '1 Pet.',
    # 'verse-by-verse-studies/2-peter' : '2 Pet.',
    # 'verse-by-verse-studies/1-john' : '1 John',
    # 'verse-by-verse-studies/2-john' : '2 John',
    # 'verse-by-verse-studies/3-john' : '3 John',
    # 'verse-by-verse-studies/jude' : 'Jude',
    # 'verse-by-verse-studies/revelation' : 'Revelation',

    'ministry-progress-summaries' : 'Ministry Progress Summaries',

    'discussion/apologetics-canada/shorter-topical-studies' : 'Discussion',
    'discussion/ryan-reeves/shorter-topical-studies' : 'Discussion',
    'discussion/ichthys/shorter-topical-studies' : 'Discussion',
    'discussion/ichthys/longer-topical-studies/satanic-rebellion-series' : 'Discussion',

    'discussion/central-baptist-warner-robins/longer-topical-studies/how-to-discern-the-voice-of-god' : 'Discussion',

    'questions-and-answers/reader-correspondence' : 'Reader Q&A',

    # 'ichthys-bible-study' : 'Ichthys Bible Study',
    # 'crosstalk-bible-study' : 'CrossTalk Bible Study',

    #'daily-progress-summaries/2022' : 'Daily Progress Summaries',
    
    #'not-displayed' : 'Not Displayed',
  }
)

steventammen = Project(
  "StevenTammen.com",
  "C:/Users/steve/Dropbox/projects/steventammen.com/",
  {
    'pages': 'Pages'
  }
)

tigercourses = Project(
  "TigerCourses.com",
  "C:/Users/steve/Dropbox/projects/tigercourses.com/",
  {
    'courses': 'Courses'
  }
)

projects = []
projects.append(bibledocs)

# TODO: setting for if program does a full re-run, or only runs on things
# Git says is dirty. Obviously, you need Git installed and on your path
# if you enable this.


'''

Now unused code


frontmatter_title_re_pattern = re.compile(r'^title: (.+)\n', re.MULTILINE)
def get_title_from_frontmatter(file_as_string):
  match_obj = frontmatter_title_re_pattern.search(file_as_string)
  return match_obj.group(1)


# Make sure you include a trailing slash for the content path. This should be the relative path
# (from the preprocess.py file) to your main content directory. Use .. to
# represent one directory up. So "../content/" would say that the content
# directory is located one directory up from this preprocessor app.
# "../content/" is what most people probably ought to use.

    # Split out all the separate content sections within the file.
    # In my organization, I always only have one per file, but there's
    # no reason why you couldn't have more than one content section 
    # per leaf file if you so desired. I'll make that possible at some future point.
    content_sections = get_content_sections_from_file(file_as_string)

    for content_section in content_sections:





# Support both YAML and TOML frontmatter. We avoid regular expressions here since 
# it is easy to do so, and doing this manually will be more performant
def strip_frontmatter_from_file(file_as_string):

  # YAML
  if(file_as_string[:3] == "---"):
    marker_char = "-"
  # TOML
  elif(file_as_string[:3] == "+++"):
    marker_char = "+"

  num_consecutive_marker_chars = 0

  # We will start searching for the ending set of ---'s or +++'s after the
  # opening set
  index = 4
  for char in file_as_string[3:]:
    if(char == marker_char):
      num_consecutive_marker_chars = num_consecutive_marker_chars + 1
      if(num_consecutive_marker_chars == 3):
        return file_as_string[(index + 1):]
    else:
      num_consecutive_marker_chars = 0
    index = index + 1

'''



'''
TODO: methods for SPLIT_ONE_INTO_MANY? Maybe?

from enum import Enum

class OrganizationalParadigm(Enum):
	SPLIT_ONE_INTO_MANY = 1
	COMBINE_MANY_INTO_ONE = 2




def build_list_of_files_to_process():
  base_path = content_directory
  markdown_content_files = []
  for content_type in content_types:
    path = base_path + content_type
    for root, directories, files in os.walk(path):
        for file in files:
          # TODO: only run stuff on files that have been changed (according to Git changeset) = diff, unless the user changes something in config file to do a full run
            if ('.md' in file) and ('_index' not in file):
                markdown_content_files.append(os.path.join(root, file))
  return markdown_content_files

def build_output_file_path(file_path, content_section):
  # Get title. At this point, it will be the only h3 header
  slides_title = (h3_header_re_pattern.search(content_section)).group(1)
  output_file_path = file_path.replace('content', 'content/slides')
  output_file_path = output_file_path.replace('.md', f'/{slugify.slugify(slides_title)}.html')
  return output_file_path



commented_out_slide_break_re_pattern = re.compile(r'<!-- --- -->')

# Have h2 headers on page for each content section, rather than grabbing title from frontmatter
content_section_re_pattern = re.compile(r'^## (.+)\n(?:.|\n)+?{{% content %}}((?:.|\n)+?){{% /content %}}', re.MULTILINE)
def get_content_sections_from_file(file_path):
  
  file_as_string = read_in_file(file_path)

  content_sections = []

  # First uncomment the slide breaks so that they will be active
  file_as_string = commented_out_slide_break_re_pattern.sub('---', file_as_string)

  # For now, we are only supporting one content section. Codebase is icky as we are in partial refactor away from
  # supporting many content sections per file, as opposed to just one.
  title = get_title_from_frontmatter(file_as_string)

  # Narrow things down to only the content we want in slides = title and full text (but not transcript, etc.)
  content_section_re_pattern.sub(
    lambda match: construct_single_content_section(match, title, content_sections),
    file_as_string
  )

  return content_sections

# https://blog.finxter.com/python-regex-start-of-line-and-end-of-line/
h3_header_re_pattern = re.compile(r'^### (.+)', re.MULTILINE)
def construct_single_content_section(match_obj, title, content_sections):
  full_text = match_obj.group(1)

  # Remove the header saying that this section is the the content. At this point, it will be the only h3 header in the full-text string
  # Also add a slide break for the title slide
  full_text = h3_header_re_pattern.sub('---', full_text)

  content_section = f'### {title}{full_text}'
  content_sections.append(content_section)
  return content_section



# This setting is very important. It determines how the preprocessor will
# automatically handle page aggregation. If you write all you content on a single
# page and want it to also be automatically split out, use SPLIT_ONE_INTO_MANY. If 
# you write your content on many separate pages and want it to also get automatically
# combined, use COMBINE_MANY_INTO_ONE. This second one is probably what most people 
# will gravitate towards, and it also makes handling frontmatter more intuitive.
organizational_paradigm = OrganizationalParadigm.COMBINE_MANY_INTO_ONE


'''