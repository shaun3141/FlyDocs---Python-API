from flask import Flask, request, jsonify
import yaml
import os
import openai

from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.requests import RequestsWrapper
from langchain.llms.openai import OpenAI
from langchain.agents.agent_toolkits.openapi import planner
llm = OpenAI(temperature=0.0, model_name="gpt-4")

def run_command():
  user_query = "get info about me"
  service = "github"
  token = ""

  with open(f"docs/{service}.yaml") as f:
    raw_docs_api_spec = yaml.load(f, Loader=yaml.Loader)
  docs_api_spec = reduce_openapi_spec(raw_docs_api_spec)

  requests_wrapper = RequestsWrapper(headers={'Authorization': token})
  docs_agent = planner.create_openapi_agent(docs_api_spec, requests_wrapper, llm)
  result = docs_agent.run(user_query)
  print(result)


run_command()