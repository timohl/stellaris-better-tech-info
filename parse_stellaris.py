from config import Config
from glob import glob
import re

# Formatted as {tech : (tier, area), ...}
def get_tech_tier_area():
    c = Config()
    stellaris_dir = c.stellaris_dir
    table = {}
    # Parse techs for tier and area values
    patterns = {
        "tech": [r"(tech_.+) =", ""],
        "tier": [r"tier = (0|1|2|3|4|5|@repeatableTechTier|@guardiantechtier|@fallentechtier)$", ""],
        "area": [r"area = (physics|engineering|society)$", ""]
    }
    for path in glob(f"{stellaris_dir}/common/technology/*.txt"):
        with open(path, 'r') as f:
            for line in f:
                for attr, pattern in patterns.items():
                    match = re.search(pattern[0], line)
                    if match != None:
                        patterns[attr][1] = match.group(1)
                        break
                if all(value != "" for value in list(patterns.values())[:][1]):
                    table[patterns["tech"][1]] = [patterns["tier"][1], patterns["area"][1]]
                    patterns["tech"][1] = patterns["tier"][1] = patterns["area"][1] = ""

    # Replace placeholder tiers
    special_tiers = {
            "@repeatableTechTier": "",
            "@guardiantechtier": "",
            "@fallentechtier": ""
    }
    with open(f"{stellaris_dir}/common/scripted_variables/00_scripted_variables.txt", 'r') as f:
        fstr = f.read()
        for tier in special_tiers:
            match = re.search(f"^{tier} = (0|1|2|3|4|5)", fstr, re.MULTILINE)
            if match != None:
                special_tiers[tier] = match.group(1)
    for tech in table:
        if table[tech][0] in special_tiers.keys():
            table[tech][0] = special_tiers[table[tech][0]]

    return table

                    

        
        



# Formatted as {int : int, ...}
def get_tier_previously_unlocked():
    table = {}
    return table


if __name__ == '__main__':
    print("Parsing stellaris")
    print("First five elements of tech_tier_area table:")
    print(dict(list(get_tech_tier_area().items())[:5]))
    print("First five elements of tier_previously_unlocked table:")
    print(dict(list(get_tier_previously_unlocked().items())[:5]))
