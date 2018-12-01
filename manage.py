#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index - 副本 (3).html")
    # return redirect(url_for("test"))
    # return redirect("out.html")

@app.route("/test")
def test():
    return render_template("out.html")


if __name__ == '__main__':
    app.run(port=5000)
