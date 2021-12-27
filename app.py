#######################################################
#             Nebula Server Directories               #
#                  by Adrien Jayat                    #
#######################################################

import os

import toml
from flask import Flask, send_file, render_template

CONFIG = toml.load("config.toml")
URL = CONFIG["url"].rstrip('/')

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("listdirs.html",
                           dirs=CONFIG["folders"],
                           parent_url=URL)


@app.route("/<path:path>")
def dirs_view(path: str):
    """
    List all folders and files for the specified path 
    """
    subfolders = path.rstrip("/").split("/")

    if not (base := CONFIG["folders"].get(subfolders[0])):
        return "Invalid url"

    parent_path = os.path.join(base.get("path"), *subfolders[1:])
    if not os.path.exists(parent_path):
        return "Can't find the ressource"

    if os.path.isfile(parent_path):
        return send_file(parent_path, as_attachment=True)

    return render_template("listdirs.html",
                           dirs=os.listdir(parent_path),
                           parent_url=URL+'/'+path)
