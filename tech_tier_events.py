from config import Config
from parse_stellaris import get_languages, get_file_str, write_file
import re
import os
import shutil

def _create_dirs(mod_dir):
    os.makedirs(f"{mod_dir}/tech_tier_events/common/event_chains", exist_ok=True)
    os.makedirs(f"{mod_dir}/tech_tier_events/common/on_actions", exist_ok=True)
    os.makedirs(f"{mod_dir}/tech_tier_events/events", exist_ok=True)

def _copy_meta_files(mod_dir):
    shutil.copyfile("tech_tier_events.mod", f"{mod_dir}/tech_tier_events.mod")
    shutil.copyfile("tech_tier_events/thumbnail.jpg", f"{mod_dir}/tech_tier_events/thumbnail.jpg")

def _create_loc_dirs(mod_dir, language):
    os.makedirs(f"{mod_dir}/tech_tier_events/localisation/{language}", exist_ok=True)

def _get_localisation_file_str():
    return get_file_str(f"tech_tier_events/localisation/english/event_chains_l_english_tech_tier_events.yml")

def _write_localisation_mod_file(mod_dir, language, generic_str):
    str = re.sub("l_english:", f"l_{language}:", generic_str)
    write_file(f"{mod_dir}/tech_tier_events/localisation/{language}/event_cains_l_{language}_tech_tier_events.yml", str)


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
# Copy event chain
# Copy on actions
# Copy events with replaced placeholders



#    table = get_tech_tier_area()
#    tier_prev_table = get_tier_previously_unlocked()

    _copy_meta_files(mod_dir)


if __name__ == '__main__':
    generate()
