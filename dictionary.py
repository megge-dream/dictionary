# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask, jsonify, request, abort


app = Flask(__name__)
data = {}


@app.route('/dictionary/<string:key>', methods=['GET'])
def get_value(key):
    """
    Get value from dictionary by key.
    :param key: key
    :return: json with parameters:
            result - value from key
            time - time of answer
    """
    if key not in data.keys():
        abort(404)
    value = data.get(key)
    return jsonify({'result': value, 'time': "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())})


@app.route('/dictionary', methods=['POST'])
def add_dictionary_object():
    """
    Add value-key in dictionary.
    :return: json with parameters:
            result - value from key
            time - time of answer
    """
    if 'value' not in request.json or 'key' not in request.json:
        return abort(400)
    key = request.json.get('key')
    value = request.json.get('value')
    if key in data.keys():
        return abort(409)
    data.update({key: value})
    return jsonify({'result': value, 'time': "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())})


@app.route('/dictionary/<string:key>', methods=['PUT'])
def change_value(key):
    """
    Change value from dictionary by key.
    :param key: key
    :return: json with parameters:
            result - value from key
            time - time of answer
    """
    if key not in data.keys():
        abort(404)
    if 'value' not in request.json:
        return abort(400)
    new_value = request.json.get('value')
    data.update({key: new_value})
    return jsonify({'result': new_value, 'time': "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())})


@app.route('/dictionary/<string:key>', methods=['DELETE'])
def delete_dictionary_object(key):
    """
    Delete value from dictionary by key.
    :param key: key
    :return: json with parameters:
            result - null
            time - time of answer
    """
    try:
        del data[key]
    except KeyError:
        pass
    return jsonify({'result': None, 'time': "{:%Y-%m-%d %H:%M}".format(datetime.utcnow())})


@app.route('/dictionary', methods=['GET'])
def get_dictionary():
    """
    Get dictionary.
    :return: json dictionary
    """
    return jsonify(data)

if __name__ == '__main__':
    app.run()