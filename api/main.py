from flask import Flask, request, jsonify
import yaml
import os
import openai
from flask_cors import CORS

from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.requests import RequestsWrapper
from langchain.llms.openai import OpenAI
from langchain.agents.agent_toolkits.openapi import planner

llm = OpenAI(temperature=0.0, model_name="gpt-4")

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello from Flask!"


@app.route("/run")
def run():
    return "Hello from Run2!"


# post payload: command, service & token
"""
{
  "service": "intercom",
  "command": "get admin",
  "token": "Bearer dG9rOjk0ZjAwOGVhX2I4MDdfNDZiY185ODU1X2M4ZWJkMjhlZGJmYToxOjA="
}
"""


@app.route("/run_command", methods=["POST"])
def run_command():
    user_query = request.json.get("command")
    service = request.json.get("service")
    token = request.json.get("token")

    with open(f"docs/{service}.yaml") as f:
        raw_docs_api_spec = yaml.load(f, Loader=yaml.Loader)
    docs_api_spec = reduce_openapi_spec(raw_docs_api_spec)

    requests_wrapper = RequestsWrapper(headers={"Authorization": token})

    if user_query is None:
        return jsonify({"error": "No command provided"}), 400

    try:
        docs_agent = planner.create_openapi_agent(docs_api_spec, requests_wrapper, llm)
    except ValueError as openapi_error:
        return jsonify({"error": str(openapi_error)}), 400
    result = docs_agent.run(user_query)

    return jsonify({"result": result})


app.run(host="0.0.0.0", port=81)
