import sys
from parser import Parser

if __name__== "__main__":
    arguments = sys.argv

    # handle cli cases
    try:
        if len(arguments) != 2:
            raise ValueError("input format is not respected, try ~ python3 pac-man.py [config_file] ~")
        config_file = arguments[1]
        if not config_file.endswith(".json"):
            raise TypeError("the config file provided is not json !")
    except (ValueError, TypeError) as e:
        print(e)
        sys.exit(1)

    # handle config file acces problems
    try:
        with open(config_file) as f:
            parser = Parser(config_file)
            new = parser.parse_config()
            print("\nSuccessfully parsed configuration:")
            for key, value in new.items():
                print(f"  {key}: {value} ({type(value).__name__})")
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        print("Accessing config_file denied, reason:", e)
        sys.exit(1)