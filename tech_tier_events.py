from config import Config
from parse_stellaris import get_tech_tier_area, get_tier_previously_unlocked, get_languages, get_file_str, write_file
import re
import os
import shutil

def _create_dirs(mod_dir):
    os.makedirs(f"{mod_dir}/tech_tier_events/common/event_chains", exist_ok=True)
    os.makedirs(f"{mod_dir}/tech_tier_events/common/on_actions", exist_ok=True)
    os.makedirs(f"{mod_dir}/tech_tier_events/events", exist_ok=True)

def _create_loc_dirs(mod_dir, language):
    os.makedirs(f"{mod_dir}/tech_tier_events/localisation/{language}", exist_ok=True)

def _get_localisation_file_str():
    return get_file_str("tech_tier_events/localisation/english/event_chains_l_english_tech_tier_events.yml")

def _write_localisation_mod_file(mod_dir, language, generic_str):
    str = re.sub("l_english:", f"l_{language}:", generic_str)
    write_file(f"{mod_dir}/tech_tier_events/localisation/{language}/event_cains_l_{language}_tech_tier_events.yml", str)

def _copy_file(mod_dir, path):
    shutil.copyfile(path, f"{mod_dir}/{path}")

def _get_tech_tier_events_file_str():
    return get_file_str("tech_tier_events/events/tech_tier_events.txt", "utf-8")

def _write_tech_tier_events_mod_file(mod_dir, events_str):
    write_file(f"{mod_dir}/tech_tier_events/events/tech_tier_events.txt", events_str, "utf-8", '\r\n')

def _insert_techs(events_str, table):
    lines = events_str.splitlines(True) 
    better_lines = [lines[0]]
    for line in lines[1:]:
        match = re.search(r"last_increased_tech = @techs_(engineering|physics|society)_tier_(1|2|3|4)@", line)
        if match != None:
            match_area = match.group(1)
            match_tier = match.group(2)
            for tech in table:
                tier = table[tech][0]
                area = table[tech][1]
                if area == match_area and tier == match_tier:
                    front, placeholder, back = line.split("@", 2)
                    better_lines.append(f"{front}{tech}{back}")
        else:
            better_lines.append(line)
    return "".join(better_lines)
        

def generate():
    print("Generate \"Tech Tier Events\" mod.")
    c = Config()
    stellaris_dir = c.stellaris_dir
    mod_dir = c.mod_dir
    _create_dirs(mod_dir)
    languages = get_languages(stellaris_dir)
    generic_loc_str = _get_localisation_file_str()
    for language in languages:
        _create_loc_dirs(mod_dir, language)
        _write_localisation_mod_file(mod_dir, language, generic_loc_str)
    _copy_file(mod_dir, "tech_tier_events.mod")
    shutil.copyfile("tech_tier_events.mod", f"{mod_dir}/tech_tier_events/descriptor.mod")
    _copy_file(mod_dir, "tech_tier_events/thumbnail.jpg")
    _copy_file(mod_dir, "tech_tier_events/common/event_chains/tech_tier_chains.txt")
    _copy_file(mod_dir, "tech_tier_events/common/on_actions/tech_tier_on_actions.txt")

    events_str = _get_tech_tier_events_file_str()
    events_str = _insert_techs(events_str, get_tech_tier_area())

    tier_prev_table = get_tier_previously_unlocked()
    _write_tech_tier_events_mod_file(mod_dir, events_str)


if __name__ == '__main__':
    generate()
