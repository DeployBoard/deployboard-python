import os

# Initialize our config.
config = {
    "MONGO_URI": None,
    "MONGO_DATABASE": "deployboard"
}

# Loop through our defaults.
for item in config:
    # Check if the item is in the environment.
    if item in os.environ:
        # Override the default with what is in the environment.
        config[item] = os.environ[item]
