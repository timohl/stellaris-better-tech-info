from config import Config
from parse_stellaris import get_tech_tier_area, get_tier_previously_unlocked, get_languages, get_file_str, write_file
from glob import glob
from io import StringIO
import re
import unittest
import os
import shutil
import codecs

def _create_dirs(mod_dir, language):
    os.makedirs(f"{mod_dir}/better_tech_info/localisation/{language}", exist_ok=True)

def _copy_meta_files(mod_dir):
    shutil.copyfile("better_tech_info.mod", f"{mod_dir}/better_tech_info.mod")
    shutil.copyfile("better_tech_info/thumbnail.jpg", f"{mod_dir}/better_tech_info/thumbnail.jpg")

# TODO: Make get and write more generic and on all localisation files containing techs (detect techs in files).

def _get_main_localisation_file_str(stellaris_dir, language):
    return get_file_str(f"{stellaris_dir}/localisation/{language}/l_{language}.yml")

def _get_tech_localisation_file_str(stellaris_dir, language):
    return get_file_str(f"{stellaris_dir}/localisation/{language}/technology_l_{language}.yml")

def _get_megacorp_localisation_file_str(stellaris_dir, language):
    return get_file_str(f"{stellaris_dir}/localisation/{language}/megacorp_l_{language}.yml")

def _get_apocalypse_localisation_file_str(stellaris_dir, language):
    return get_file_str(f"{stellaris_dir}/localisation/{language}/apocalypse_l_{language}.yml")

def _write_file(path, str):
    with open(path, 'w', encoding="utf-8-sig", errors='strict', newline='\n') as f:
        f.write(str)

def _write_main_localisation_mod_file(mod_dir, language, better_main_loc_str):
    write_file(f"{mod_dir}/better_tech_info/localisation/{language}/better_tech_info_l_{language}.yml", better_main_loc_str)

def _write_tech_localisation_mod_file(mod_dir, language, better_tech_loc_str):
    write_file(f"{mod_dir}/better_tech_info/localisation/{language}/technology_l_{language}.yml", better_tech_loc_str)

def _write_megacorp_localisation_mod_file(mod_dir, language, better_megacorp_loc_str):
    write_file(f"{mod_dir}/better_tech_info/localisation/{language}/megacorp_l_{language}.yml", better_megacorp_loc_str)

def _write_apocalypse_localisation_mod_file(mod_dir, language, better_apocalypse_loc_str):
    write_file(f"{mod_dir}/better_tech_info/localisation/{language}/apocalypse_l_{language}.yml", better_apocalypse_loc_str)

def _get_tech_info_str(tech, table):
    return f"(Tier {table[tech][0]})"

def _insert_better_tech_info(tech_localisation_str, table):
    lines = tech_localisation_str.splitlines(True)
    better_lines = [lines[0]]
    for line in lines[1:]:
        match = None
        for tech in table:
            pattern = f"^ {tech}_desc"
            match = re.search(pattern, line)
            if match != None:
                info = _get_tech_info_str(tech, table)
                front, sep, back = line.rpartition('"')
                better_lines.append(f"{front} {info}{sep}{back}")
                break
        if match == None:
            better_lines.append(line)
    return "".join(better_lines)

def _insert_gerneral_tier_data(main_localisation_str, table):
    lines = main_localisation_str.splitlines(True)
    better_lines = [lines[0]]
    for line in lines[1:]:
        match = re.search("topbar_button_technology_delayed", line)
        if match != None:
            info = ", ".join([f"T{tier}({prev})" for tier, prev in table.items()])
            front, sep, back = line.rpartition('.§!"')
            better_lines.append(f"{front}.\\n{info}{sep}{back}")
    better_lines.append("")
    return "".join(better_lines)



def generate():
    print("Generate \"Better Tech Info\" mod.")
    c = Config()
    stellaris_dir = c.stellaris_dir
    mod_dir = c.mod_dir
    languages = get_languages(stellaris_dir)
    table = get_tech_tier_area()
    tier_prev_table = get_tier_previously_unlocked()
    for language in languages:
        # Create localisation directory for language
        _create_dirs(mod_dir, language)
        # Generate better_tech_info_l_{language}.yml from main localisation file
        main_loc_str = _get_main_localisation_file_str(stellaris_dir, language)
        better_main_loc_str = _insert_gerneral_tier_data(main_loc_str, tier_prev_table)
        _write_main_localisation_mod_file(mod_dir, language, better_main_loc_str)
        # Generate technology_l_{language}.yml
        tech_loc_str = _get_tech_localisation_file_str(stellaris_dir, language)
        better_tech_loc_str = _insert_better_tech_info(tech_loc_str, table)
        _write_tech_localisation_mod_file(mod_dir, language, better_tech_loc_str)
        # Generate megacorp_l_{language}.yml
        megacorp_loc_str = _get_megacorp_localisation_file_str(stellaris_dir, language)
        better_megacorp_loc_str = _insert_better_tech_info(megacorp_loc_str, table)
        _write_megacorp_localisation_mod_file(mod_dir, language, better_megacorp_loc_str)
        # Generate apocalypse_l_{language}.yml
        apocalypse_loc_str = _get_apocalypse_localisation_file_str(stellaris_dir, language)
        better_apocalypse_loc_str = _insert_better_tech_info(apocalypse_loc_str, table)
        _write_apocalypse_localisation_mod_file(mod_dir, language, better_apocalypse_loc_str)

    _copy_meta_files(mod_dir)


"""
Testing
"""
class TestBetterTechInfo(unittest.TestCase):
    def test_get_tech_info_str(self):
        table = {
                "tech_morphogenetic_field_mastery": ["1", "society"],
                "tech_gene_tailoring": ["2", "society"],
        }
        techs = [
                "tech_morphogenetic_field_mastery",
                "tech_gene_tailoring",
        ]
        aims = [
                "(Tier 1)",
                "(Tier 2)",
        ] 
        results = [_get_tech_info_str(tech, table) for tech in techs]
        self.assertEqual(results, aims)


    def test_insert_better_tech_info(self):
        self.maxDiff = None
        table = {
                "tech_morphogenetic_field_mastery": ["1", "society"],
                "tech_gene_tailoring": ["2", "society"],
        }

        tech_loc_str = better_tech_loc_str_aim = """\
l_english:
 tech_morphogenetic_field_mastery:0 "Morphogenetic Field Mastery"
 tech_morphogenetic_field_mastery_desc:1 "From its cradle as a purely pharmaceutical venture, advancements in ou     r understanding of the morphogenetic field allow for direct, subconscious interfaces with organic units.{}"
 tech_gene_tailoring:0 "Gene Tailoring"
 tech_gene_tailoring_desc:1 "Making gene-editing tools widely available is sure to have a positive impact on our      development as a species.{}"
 tech_gene_tailoring_modifier_desc:0 "$species_trait_points_add$: $POINTS|0=+$"\
"""
        tech_loc_str = tech_loc_str.format("", "")
        better_tech_loc_str_aim = better_tech_loc_str_aim.format(
                " " + _get_tech_info_str("tech_morphogenetic_field_mastery", table),
                " " + _get_tech_info_str("tech_gene_tailoring", table)
        )
        better_tech_loc_str = _insert_better_tech_info(tech_loc_str, table)
        self.assertEqual(better_tech_loc_str, better_tech_loc_str_aim)

    def test_insert_gerneral_tier_data(self):
        self.maxDiff = None
        file_str = """\
l_english:
 topbar_button_technology_instant:0 "§H$topbar_button_technology_name$§!"
 topbar_button_technology_delayed:0 "§EOpens the Technology view where you can research technological advanceme      nts.§!"\
"""
        better_file_str_aim = """\
l_english:
 topbar_button_technology_delayed:0 "§EOpens the Technology view where you can research technological advanceme      nts.\\nT1(0), T2(6), T3(6), T4(6), T5(6).§!"\
"""
        table = {
                "1":"0",
                "2":"6",
                "3":"6",
                "4":"6",
                "5":"6",
        }
        better_file_str = _insert_gerneral_tier_data(file_str, table)
        self.assertEqual(better_file_str, better_file_str_aim)

if __name__ == '__main__':
    # Usage
    generate()
    # Testing
    unittest.main()
