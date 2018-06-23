from config import Config
from glob import glob
from io import StringIO
import re
import unittest

def _get_raw_tech_tier_area(file_str):
    table = {}
    patterns = {
        "tech": [r"(tech_.+) =", ""],
        "tier": [r"tier = (0|1|2|3|4|5|@repeatableTechTier|@guardiantechtier|@fallentechtier)$", ""],
        "area": [r"area = (physics|engineering|society)", ""]
    }
    for line in StringIO(file_str):
        for attr, pattern in patterns.items():
            match = re.search(pattern[0], line)
            if match != None:
                patterns[attr][1] = match.group(1)
                break
        if all(value != "" for value in list(patterns.values())[:][1]):
            table[patterns["tech"][1]] = [patterns["tier"][1], patterns["area"][1]]
            patterns["tech"][1] = patterns["tier"][1] = patterns["area"][1] = ""
    return table


def _get_raw_tech_tier_area_file_str(stellaris_dir):
    file_str_list = []
    for path in glob(f"{stellaris_dir}/common/technology/*.txt"):
        with open(path, 'r') as f:
            file_str_list.append(f.read())
    return "".join(file_str_list)

def _get_special_tiers(file_str):
    special_tiers = {
            "@repeatableTechTier": "",
            "@guardiantechtier": "",
            "@fallentechtier": ""
    }
    for tier in special_tiers:
        match = re.search(f"^{tier} = (0|1|2|3|4|5)", file_str, re.MULTILINE)
        if match != None:
            special_tiers[tier] = match.group(1)
    return special_tiers

def _get_special_tiers_file_str(stellaris_dir):
    with open(f"{stellaris_dir}/common/scripted_variables/00_scripted_variables.txt", 'r') as f:
        return f.read()

def _replace_special_tiers(table, special_tiers):
    for tech in table:
        if table[tech][0] in special_tiers.keys():
            table[tech][0] = special_tiers[table[tech][0]]
    return table

# Formatted as {tech : (tier, area), ...}
def get_tech_tier_area():
    c = Config()
    stellaris_dir = c.stellaris_dir
    # Parse techs for tier and area values
    file_str = _get_raw_tech_tier_area_file_str(stellaris_dir)
    table = _get_raw_tech_tier_area(file_str)
    # Replace placeholder tiers
    file_str = _get_special_tiers_file_str(stellaris_dir)
    special_tiers = _get_special_tiers(file_str)
    table = _replace_special_tiers(table, special_tiers)
    return table

def _get_tier_definition_file_str(stellaris_dir):
    with open(f"{stellaris_dir}/common/technology/tier/00_tier.txt", 'r') as f:
        return f.read()

def _get_tier_previously_unlocked(file_str):
    table = {}
    patterns = [
            [r"^(\d) = \{", ""],
            [r"previously_unlocked = (\d+)", ""],
    ]
    tier = ""
    for line in StringIO(file_str):
        if tier == "":
            match = re.search(r"^([1|2|3|4|5]) = \{", line)
            if match != None:
                tier = match.group(1)
        else:
            match = re.search(r"previously_unlocked = (\d+)", line)
            if match != None:
                table[tier] = match.group(1)
                tier = ""
    return table

# Formatted as {int : int, ...}
def get_tier_previously_unlocked():
    c = Config()
    stellaris_dir = c.stellaris_dir
    file_str = _get_tier_definition_file_str(stellaris_dir)
    table = _get_tier_previously_unlocked(file_str)
    return table

"""
Testing
"""
class TestParseStellaris(unittest.TestCase):
    def test_get_raw_tech_tier_area(self):
        file_str = """
# ##################
# Ship Sizes
# ##################
tech_corvettes = {
	cost = 0
	area = engineering	
	start_tech = yes
	category = { voidcraft }
	prerequisites = { "tech_starbase_2" }
	tier = 0
	
	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_CORVETTE_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_CORVETTE_CONSTRUCTION_DESC"
		}
	}	
}
tech_repeatable_improved_tile_food_output = {
	area = society
	cost = @repeatableTechBaseCost
	cost_per_level = @repeatableTechLevelCost
	tier = @repeatableTechTier
	category = { biology }
	levels = -1
	prerequisites = { "tech_gene_crops" }
	weight = @repeatableTechWeight
	
	weight_modifier = {
		factor = @repatableTechFactor
	}
	
	ai_weight = {
		factor = 1.0
	}
	
	weight_groups = {
		repeatable
	}
	mod_weight_if_group_picked = {
		repeatable = 0.01
	}
	
	modifier = {
		tile_resource_food_mult = 0.05
	}
}
# Dark Matter Deflectors
tech_dark_matter_deflector = {
	cost = @fallentechcost
	area = physics
	tier = @fallentechtier
	category = { field_manipulation }
	ai_update_type = all
	weight = 1
	is_rare = yes
	
	prerequisites = { "tech_shields_5" }
	
	weight_modifier = {	
		modifier = {
			factor = 0
			NOR = { 
				is_country_type = fallen_empire 
				is_country_type = awakened_fallen_empire 
			}
		}
	}
}
        """
        table_aim = {
                "tech_dark_matter_deflector": ["@fallentechtier", "physics"],
                "tech_corvettes": ["0", "engineering"],
                "tech_repeatable_improved_tile_food_output": ["@repeatableTechTier", "society"],
        }
        table = _get_raw_tech_tier_area(file_str)
        self.assertEqual(table, table_aim)

    def test_get_special_tiers(self):
        file_str = ("@repeatableTechTier = 0\n"
                    "@guardiantechtier = 5\n"
                    "@blabla = 5\n"
                    "@fallentechtier = 3\n"
        )
        special_tiers_aim = {
                "@repeatableTechTier":  "0",
                "@guardiantechtier":    "5",
                "@fallentechtier":      "3",
        }
        special_tiers = _get_special_tiers(file_str)
        self.assertEqual(special_tiers, special_tiers_aim)

    def test_replace_special_tiers(self):
        table = {
                "tech_bla":         ["5",                   "society"],
                "tech_blub":        ["@fallentechtier",     "engineering"],
                "tech_forty_two":   ["@guardiantechtier",   "physics"],
                "tech_foo":         ["@repeatableTechTier",  "engineering"],
                "tech_bar":         ["0",                   "society"],
                "tech_of_techs":    ["@repeatableTechTier", "society"],
        }
        special_tiers = {
                "@repeatableTechTier":  "0",
                "@guardiantechtier":    "5",
                "@fallentechtier":      "3",
        }
        ret_table_aim = {
                "tech_bla":         ["5", "society"],
                "tech_blub":        ["3", "engineering"],
                "tech_forty_two":   ["5", "physics"],
                "tech_foo":         ["0", "engineering"],
                "tech_bar":         ["0", "society"],
                "tech_of_techs":    ["0", "society"],
        }
        ret_table = _replace_special_tiers(table, special_tiers)
        self.assertEqual(ret_table,  ret_table_aim)

    def test_get_tier_previously_unlocked(self):
        file_str = """
# The previously_unlocked-value decide ...
0 = { # Tier 0
}
1 = { # Tier 1
        previously_unlocked = 5
}
2 = { # Tier 2
        previously_unlocked = 6
}
3 = { # Tier 3
        previously_unlocked = 7
}
        """
        table_aim = {
                "1": "5",
                "2": "6",
                "3": "7",
        }
        table = _get_tier_previously_unlocked(file_str)
        self.assertEqual(table, table_aim)

if __name__ == '__main__':
    # Example usage
    """
    print("Parsing stellaris")
    print("First five elements of tech_tier_area table:")
    print(dict(list(get_tech_tier_area().items())[:5]))
    print("First five elements of tier_previously_unlocked table:")
    print(dict(list(get_tier_previously_unlocked().items())[:5]))
    """
    # Testing
    unittest.main()
