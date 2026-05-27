    # Single regular expression to extract:

    # No numbers in the titles of things: both YT videos, and sections on site.
    # Means can add and remove sections without worrying about numbering/order

    # Have range of .Sections in list pages template, but no range of .Pages. That's handled here
    # So sections have expandable/collapsible UI and content level, but not individual pages,
    # Which have full collapsible content/transcript

    # How does this work with nested things and list page templates? Like Q&As/self-generated/something
    # => just don't put the comment for aggregation there, and it will just use the Hugo template for pages

    # Will have to rework templates, probably


    # Not this: Multiple levels, with summary coming from _index.md pages for self-generated and reader-correspondence?



    # Get GitHub repos made private, including theme and preprocessor submodules.
    # Ensure Netlify deploys still function properly



import pathlib
from config import *
from lib.main import *



# For now, just manually switch the build project in the config file, and hardcode
# things here.
content_directory = projects[0].project_path + 'content/'
slides_directory = content_directory + 'slides/'
content_types = projects[0].content_types
content_type_paths = projects[0].content_types.keys()

# Initialize variables to build subject map
subject_map = {}

# We want to clear out the slides content directory every time we run the script,
# to make sure we always start from a clean base
pathlib.Path(slides_directory).mkdir(parents=True, exist_ok=True)
clean_slides_directory(slides_directory)

# We update the summaries between <!-- summary --> HTML comments every time we run the script
# The text overwriting what was there before is the current text between the
# closing YAML --- and the <!--more--> divider
update_summaries(content_directory)

# Each study is composed of one or more content pages, each of which may have one or more associated discussion pages.
# The full content of each study ends up aggregated on its aggregation page.
studies = build_list_of_content_groups_to_process(content_directory, content_type_paths)

for study in studies:

  aggregation_page_path = study.aggregation_page_path
  content_pages = study.content_pages

  # If study only has a single lesson
  if (study.aggregation_page_path == ''):

    for content_page_path, discussion_page_paths in content_pages.items():

      existing_single_lesson_page_content = read_in_file(content_page_path)
      study_title = get_page_title(existing_single_lesson_page_content)

      # Dictionary will either use weight as keys or page titles as keys, one or the other
      # We will then sort before the aggregation
      discussion_pages_to_aggregate = {}

      for discussion_page_path in discussion_page_paths:

        discussion_page = process_leaf_page(discussion_page_path, study_title, subject_map, '')

        # For now, assume that pages without summaries also won't have slides. Rn, just daily progress summaries
        if((discussion_page.content_section_for_slides != None) and 
            (discussion_page.summary != None)):
          process_content_section_and_build_slides(
            discussion_page_path,
            discussion_page.content_section_for_slides,
            discussion_page.summary)

        # If pages have weight defined, then things should
        # be sorted by weight eventually => we key based on weight. If weight is
        # not defined, then we key (and eventually sort, below) based on title.
        # Make assumption of uniqueness for weights (and titles).
        # Eventually, check it explicitly and throw error?
        if(discussion_page.weight != None):
          discussion_pages_to_aggregate[int(discussion_page.weight)] = discussion_page.full_content_for_aggregation
        else:
          discussion_pages_to_aggregate[discussion_page.title] = discussion_page.full_content_for_aggregation

      # Will be either weights or titles. Either way, we want to sort ascending,
      # so that pages are aggregated in order
      page_identifiers = sorted(discussion_pages_to_aggregate.keys())
        
      # Build discussion pages section. Here, unlike with content pages, the list might be completely empty,
      # if there are are no discussion pages for a specific content page
      discussion_pages_section = ''
      if(len(discussion_pages_to_aggregate) != 0):
        discussion_pages_section = discussion_pages_to_aggregate[page_identifiers[0]]
        for page_identifier in page_identifiers[1:]:
          discussion_pages_section = discussion_pages_section + "\n\n<br/>\n\n" + discussion_pages_to_aggregate[page_identifier]
        
      content_page = process_leaf_page(content_page_path, study_title, subject_map, discussion_pages_section)

      # For now, assume that pages without summaries also won't have slides. Rn, just daily progress summaries
      if((content_page.content_section_for_slides != None) and 
          (content_page.summary != None)):
        process_content_section_and_build_slides(
        content_page_path,
        content_page.content_section_for_slides,
        content_page.summary)



  # If study has more than one lesson
  else:

    # Dictionary will either use weight as keys or page titles as keys, one or the other
    # We will then sort before the aggregation
    content_pages_to_aggregate = {}

    existing_aggregate_page_content = read_in_file(aggregation_page_path)
    study_title = get_page_title(existing_aggregate_page_content)

    for content_page_path, discussion_page_paths in content_pages.items():

      # Dictionary will either use weight as keys or page titles as keys, one or the other
      # We will then sort before the aggregation
      discussion_pages_to_aggregate = {}

      for discussion_page_path in discussion_page_paths:

        discussion_page = process_leaf_page(discussion_page_path, study_title, subject_map, '')

        # For now, assume that pages without summaries also won't have slides. Rn, just daily progress summaries
        if((discussion_page.content_section_for_slides != None) and 
            (discussion_page.summary != None)):
          process_content_section_and_build_slides(
            discussion_page_path,
            discussion_page.content_section_for_slides,
            discussion_page.summary)

        # If pages have weight defined, then things should
        # be sorted by weight eventually => we key based on weight. If weight is
        # not defined, then we key (and eventually sort, below) based on title.
        # Make assumption of uniqueness for weights (and titles).
        # Eventually, check it explicitly and throw error?
        if(discussion_page.weight != None):
          discussion_pages_to_aggregate[int(discussion_page.weight)] = discussion_page.full_content_for_aggregation
        else:
          discussion_pages_to_aggregate[discussion_page.title] = discussion_page.full_content_for_aggregation

      # Will be either weights or titles. Either way, we want to sort ascending,
      # so that pages are aggregated in order
      page_identifiers = sorted(discussion_pages_to_aggregate.keys())
        
      # Build discussion pages section. Here, unlike with content pages, the list might be completely empty,
      # if there are are no discussion pages for a specific content page
      discussion_pages_section = ''
      if(len(discussion_pages_to_aggregate) != 0):
        discussion_pages_section = discussion_pages_to_aggregate[page_identifiers[0]]
        for page_identifier in page_identifiers[1:]:
          discussion_pages_section = discussion_pages_section + "\n\n<br/>\n\n" + discussion_pages_to_aggregate[page_identifier]
        
      content_page = process_leaf_page(content_page_path, study_title, subject_map, discussion_pages_section)

      # For now, assume that pages without summaries also won't have slides. Rn, just daily progress summaries
      if((content_page.content_section_for_slides != None) and 
          (content_page.summary != None)):
        process_content_section_and_build_slides(
        content_page_path,
        content_page.content_section_for_slides,
        content_page.summary)

      # If pages have weight defined, then things should
      # be sorted by weight eventually => we key based on weight. If weight is
      # not defined, then we key (and eventually sort, below) based on title.
      # Make assumption of uniqueness fo r weights (and titles).
      # Eventually, check it explicitly and throw error?
      if(content_page.weight != None and content_page.weight != ''):
        content_pages_to_aggregate[int(content_page.weight)] = content_page.full_content_for_aggregation
      else:
        content_pages_to_aggregate[content_page.title] = content_page.full_content_for_aggregation

    # Will be either weights or titles. Either way, we want to sort ascending,
    # so that pages are aggregated in order
    page_identifiers = sorted(content_pages_to_aggregate.keys())
      
    # Build aggregate page content
    new_aggregation_page_content = ''
    if(len(content_pages_to_aggregate) > 0):
      new_aggregation_page_content = content_pages_to_aggregate[page_identifiers[0]]
      for page_identifier in page_identifiers[1:]:
        new_aggregation_page_content = new_aggregation_page_content + "\n\n<br/>\n\n" + content_pages_to_aggregate[page_identifier]
    
    # Stick the newly-built content on the aggregate page
    build_aggregation_page(aggregation_page_path, existing_aggregate_page_content, new_aggregation_page_content)

build_subject_index(subject_map, content_directory, content_types)

