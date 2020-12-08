import texture_atlas
import json

# This project aims to transform a folder of images (name = texture id), and create
# a texture atlas from it. Additionally it will transform the texture atlas to grayscale
# and blur the image in order to create an attenuation map for lighting.

f = open("config.json", "r")
config = json.loads(f.read())
f.close()

atlas = texture_atlas.TextureAtlas(config["rows"], config["cols"], config["texture_size"], config["padding_size"])
atlas.set_path(config["input_folder"])
atlas.create()
atlas.save(config["output_folder"] + "texture_atlas.png")
atlas.save_atten(config["output_folder"] + "texture_atlas_atten.png")
