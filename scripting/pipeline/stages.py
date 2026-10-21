from . import prompts, parsers
from .localization import get_localization
from .models import log

def call(project, client, stage, values, parser):
    rendered=prompts.render(stage, values); raw=client.complete(rendered); result=parser(raw); log(project, "stage_complete", stage=stage); return result, raw

def run_all(project, client, language, duration, monster, scene_count=None, checkpoint=None):
    locale = get_localization(language)
    project["localization"] = {
        "language": locale["language_name"],
        "language_code": locale["language_code"],
        "script": locale["script_name"],
        "region": locale["region"],
        "culture_mode": locale["culture_mode"],
        "dialogue_field": locale["dialogue_field"],
        "narrator_direction": locale["narrator_direction"],
        "character_voice_fallback": locale["character_voice_fallback"],
        "character_descriptor_fallback": locale["character_descriptor_fallback"],
        "title_font": locale["title_font"],
        "title_kicker": locale["title_kicker"],
        "fallback_title": locale["fallback_title"],
    }
    if project["idea"]["selected"] is None: raise RuntimeError("Choose an idea first with `choose`")
    selected=project["idea"]["selected"]
    if project["script"]["raw_text"] is None:
        raw_data, raw=call(project,client,"story",{"TITLE":selected.get("title",""),"HOOK":selected.get("hook",selected.get("tagline","")),"LANGUAGE":language,"DURATION_MINUTES":duration,"WORD_COUNT":duration*150,"MONSTER":monster},lambda x:x)
        project["script"].update(status="done",language=language,duration_minutes=duration,word_count=duration*150,monster=monster,raw_text=raw,raw_output=raw)
        if checkpoint: checkpoint()
    script=project["script"]["raw_text"]
    if not project["characters"]:
        data,raw=call(project,client,"characters",{"LANGUAGE":locale["language_name"],"SCRIPT":script},parsers.characters)
        if not data: raise ValueError("Character extraction returned no assets")
        project["characters"]=data
        if checkpoint: checkpoint()
    if not project["backgrounds"]:
        data,raw=call(project,client,"backgrounds",{"LANGUAGE":locale["language_name"],"SCRIPT":script},parsers.backgrounds)
        if not data: raise ValueError("Background extraction returned no assets")
        project["backgrounds"]=data
        if checkpoint: checkpoint()
    if not project["scenes"]:
        requested_scenes=scene_count or duration*7
        compact_chars=[{"tag":c.get("tag"),"name":c.get("name"),"look_summary":c.get("look_summary")} for c in project["characters"]]
        compact_bgs=[{"tag":b.get("tag"),"location_name":b.get("location_name"),"look_summary":b.get("look_summary")} for b in project["backgrounds"]]
        data,raw=call(project,client,"scenes",{"LANGUAGE":locale["language_name"],"SCRIPT":script,"CHARACTERS":compact_chars,"BACKGROUNDS":compact_bgs,"DURATION_MINUTES":duration,"MINIMUM_SCENES":duration*7,"SCENE_COUNT":requested_scenes},parsers.scenes)
        project["scenes_raw_output"] = raw
        if checkpoint: checkpoint()
        if len(data) != requested_scenes: raise ValueError(f"Expected exactly {requested_scenes} scenes, parsed {len(data)}")
        project["scenes"]=data
        if checkpoint: checkpoint()
    if project["publishing"]["data"] is None:
        data,raw=call(project,client,"publishing",{"LANGUAGE":locale["language_name"],"SCRIPT":script},parsers.publishing); project["publishing"].update(status="done",data=data,raw_output=raw)
        if checkpoint: checkpoint()
