import json
import sys

class Parser():
    def __init__(self, config_file):
        self.config = config_file

    def set_defaults(self):
        self.default_conf = {"lives": 3,
                             "points_per_pacgum": 10,
                             "points_per_super_pacgum": 50,
                             "points_per_ghost": 200,
                             "highscore_filename": "highscore.json"
                             }
        return self.default_conf

    def detect_dups(self, dicts):
        seen = []
        for key , _ in dicts:
            if key in seen:
                raise TypeError("duplicate detected")
            if key not in seen:
                seen.append(key)
        return dict(dicts)

    def handle_comments(self):
        cleaned_lines = []
        with open(self.config) as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    cleaned_lines.append(line)
        clear_json_str = "".join(cleaned_lines)
        if not clear_json_str:
            print("warning: empty json file detected, falling back to default value")
            return self.default_conf
        try:
            nodups_string = json.loads(clear_json_str, object_pairs_hook=self.detect_dups)
        except TypeError:
            print("warning: duplicates detected , falling back to default values")
            return self.default_conf
        return nodups_string

    def read_config(self):
        try:
            content = self.handle_comments()
        except json.JSONDecodeError:
            print(
                "warning: config_file content does not respect json format, falling back to defaults values")
            return self.default_conf
        if not isinstance(content, dict):
            print(
                "warning: config_file content is not supported as a list format, falling back to defaults values")
            return self.default_conf
        return content

    def validate_key(self, k, config_content_or, default_config_or):
        default_config = default_config_or
        config_content = config_content_or
        messages = {"lives": "warning: Pac-Man lives must be between 0 and 10 (0 excluded), falling back to defaults --> 3 lives",
                    "points_per_pacgum": "warning: points_per_pacgum must be between 0 and 20 (0 excluded), falling back to defaults --> 10 points_per_pacgum",
                    "points_per_super_pacgum": "warning: points_per_super_pacgum must be between 0 and 80 (0 excluded), falling back to defaults --> 80 points_per_pacgum",
                    "points_per_ghost": "warning: points_per_ghost must be between 0 and 200 (0 excluded), falling back to defaults --> 200 points_per_ghost",
                    "highscore_filename": ["highscore_filename's type is not a string, falling back to defaults --> highscore.json",
                                           "highscore_filename is not valid, falling back to defaults --> highscore.json"]}
        
        if k == "lives":
            if not isinstance(config_content[k], int) or not 0 < config_content[k] <= 10:
                print(messages[k])
                return default_config[k]
            else:
                return config_content[k]
            
        elif k == "points_per_pacgum":
            if not isinstance(config_content[k], int) or not 0 < config_content[k] <= 20:
                print(messages[k])
                return default_config[k]
            else:
                return config_content[k]

        elif k == "points_per_super_pacgum":
            if not isinstance(config_content[k], int) or not 0 < config_content[k] <= 80:
                print(messages[k])
                return default_config[k]
            else:
                return config_content[k]

        elif k == "points_per_ghost":
            if not isinstance(config_content[k], int) or not 0 < config_content[k] <= 200:
                print(messages[k])
                return default_config[k]
            else:
                return config_content[k]

        elif k == "highscore_filename":
            if not isinstance(config_content[k], str):
                print(messages[k][0])
                return default_config[k]
            try:
                parts = config_content[k].split('.', 1)
                if len(parts) != 2 or not parts[1] == 'json':
                    print(messages[k][1])
                    return default_config[k]
                else:
                    return config_content[k]
            except Exception:
                return default_config[k]


    def parse_config(self):
        default_config = self.set_defaults()
        config_content = self.read_config()
        new = {}
        supported_keys = ['lives',
                          'points_per_pacgum',
                          'points_per_super_pacgum',
                          'points_per_ghost',
                          'highscore_filename']

        for k in config_content:
            if k not in supported_keys:
                continue
            new[k] = self.validate_key(k, config_content, default_config)

        for k, default_val in self.default_conf.items():
            if k in supported_keys and k not in new:
                new[k] = default_val

        return new


# try:
#     parser = Parser("config.json")
#     final_config = parser.parse_config()
#     print("\nSuccessfully parsed configuration:")
#     for key, value in final_config.items():
#         print(f"  {key}: {value} ({type(value).__name__})")
# except Exception as e:
#     print(f"Error: {e}")
#     sys.exit(1)
