import re

properties_shortcode_re_pattern = re.compile(r'^\{\{< properties((?:.|\n)+?)>\}\}', re.MULTILINE)

def replace_properties_shortcodes(content_section):
  content_section = properties_shortcode_re_pattern.sub(
      lambda match: build_embedded_video_or_audio(match.group(1)),
      content_section
    )
  return content_section

def build_embedded_video_or_audio(properties_shortcode_str):
  pattern = r'^\s*([a-zA-Z_]\w*)\s*=\s*"([^"]*)"\s*$'
  properties = dict(re.findall(pattern, properties_shortcode_str, re.MULTILINE))

  if(properties.get("srcmp3audiourl") != None):
    embedded_audio = f'''
<audio
  controls
  preload="auto" 
  src="{properties.get("srcmp3audiourl")}#t={properties.get("srcstart")},{properties.get("srcend")}"
  title="{properties.get("srctitle")}"
>
    '''
    return embedded_audio
  elif((properties.get("srcyoutubevideoid") != None)):
    embedded_video = f'''
<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/{properties.get("srcyoutubevideoid")}?start={properties.get("srcstart")}&end={properties.get("srcend")}"
  title="{properties.get("srctitle")}"
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>
    '''
    return embedded_video
  else:
    return ''
