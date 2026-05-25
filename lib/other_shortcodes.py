import re

properties_shortcode_re_pattern = re.compile(r'^\{\{< properties((?:.|\n)+?)>\}\}', re.MULTILINE)

def replace_properties_shortcodes(content_section):
  content_section = properties_shortcode_re_pattern.sub(
      lambda match: build_embedded_video_or_audio(match.group(1)),
      content_section
    )
  return content_section

def build_embedded_audio(properties):
  
  has_src_start = properties.get("srcstart") != None and properties.get("srcstart") != ""
  has_src_end = properties.get("srcend") != None and properties.get("srcend") != ""

  src_mp3_audio_url = properties.get("srcmp3audiourl")
  src_start = (properties.get("srcstart") if has_src_start else "0:00")
  src_end = ("," + properties.get("srcend") if has_src_end else "")
  src_title = properties.get("srctitle")
  
  embedded_audio = f'''
<audio controls preload="auto" title="{src_title}">
  <source src="{src_mp3_audio_url}#t={src_start}{src_end}" type="audio/mpeg">
</audio>
  '''
  return embedded_audio

def build_embedded_video(properties):
  has_src_start = properties.get("srcstart") != None and properties.get("srcstart") != ""
  has_src_end = properties.get("srcend") != None and properties.get("srcend") != ""

  src_youtube_video_id = properties.get("srcyoutubevideoid")
  src_start = (properties.get("srcstart") if has_src_start else "0")
  src_end = ("&end=" + properties.get("srcend") if has_src_end else "")
  src_title = properties.get("srctitle")

  embedded_video = f'''
<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/{src_youtube_video_id}?start={src_start}{src_end}"
  title="{src_title}"
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>
  '''
  return embedded_video

def build_embedded_video_or_audio(properties_shortcode_str):
  pattern = r'^\s*([a-zA-Z_]\w*)\s*=\s*"([^"]*)"\s*$'
  properties = dict(re.findall(pattern, properties_shortcode_str, re.MULTILINE))

  is_embedded_audio = properties.get("srcmp3audiourl") != None
  is_embedded_video = properties.get("srcyoutubevideoid") != None

  if(is_embedded_audio):
    return build_embedded_audio(properties)
  elif(is_embedded_video):
    return build_embedded_video(properties)
  else:
    return ''
