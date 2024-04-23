import copy
import json
import sys
import time
import openai
import prance
import random
import requests
import datetime


def parse_oas(spec):
    for path, path_data in spec['paths'].items():
        for method, operation_data in path_data.items():
            parameters = {param['name']: param for param in operation_data.get('parameters', [])}
            request_body = operation_data.get('requestBody')
            if request_body:
                body = request_body.get('content', {})
                if 'application/json' in body:
                    body = body.get('application/json')
                    body['description'] = request_body.get('description')
                    body['required'] = request_body.get('required', False)
                    body['in'] = 'body'
                    parameters['body'] = body
                elif 'application/x-www-form-urlencoded' in body:
                    required = []
                    if 'required' in body['application/x-www-form-urlencoded']['schema']:
                        for param in body['application/x-www-form-urlencoded']['schema']['required']:
                            required.append(param)
                    for param in body['application/x-www-form-urlencoded']['schema']['properties']:
                        parameters[param] = body['application/x-www-form-urlencoded']['schema']['properties'][param]
                        if param in required:
                            parameters[param]['required'] = True
                        parameters[param]['in'] = 'body'
            op_id = operation_data.get('operationId', f"{method}_{path}")
            op_id_list.append(op_id)
            operations[op_id] = {
                'summary': operation_data.get('summary', ''),
                'description': operation_data.get('description', ''),
                'method': method,
                'path': path,
                'parameters': parameters,
                'responses': operation_data.get('responses', {})
            }


def call_chatgpt(prompt, max_retries=3, timeout=10):
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "assistant", "content": prompt}],
                api_key=openai_api_key,
                timeout=timeout
            )

            return response
        except openai.OpenAIError as e:
            print(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(timeout)


def generate_operation_sequence():
    prompt = "Generate a list of operation IDs for a test scenario in the following format: [Operation ID1, Operation ID2, Operation ID3, ...]. The output should only have an array with operation ids without any detail. Ensure that resources are created (POST) before they are accessed (GET) or modified (PUT/DELETE).\nGenerate the list based on these operations:\n"
    for op_id, details in operations.items():
        prompt += f"- Operation ID: {op_id}, Method: {details['method'].upper()}, Summary: {details['summary']}, Description: {details['description']}, Path: {details['path']}\n"

    prompt += "\nThe sequence should cover all operations in a logical and efficient order for testing."

    response = call_chatgpt(prompt)

    if response and 'choices' in response and len(response['choices']) > 0:
        sequence = response['choices'][0].get('message', {}).get('content', '')

        try:
            sequence_list = (sequence.strip("[]").replace(" ", "").replace("\n", "").replace("\r", "").replace("\"", "")
                             .replace("'", "").split(","))
            return sequence_list
        except Exception as e:
            print(f"Error parsing the sequence: {e}")
            return None
    else:
        return "No sequence generated."


def generate_random_value(schema):
    if schema['type'] == 'string':
        if 'format' in schema:
            if schema['format'] == 'date-time':
                return str(datetime.datetime.now())
            elif schema['format'] == 'date':
                return str(datetime.date.today())
        minimum=1
        maximum=10
        if 'minimum' in schema:
            minimum = schema['minimum']
        if 'maximum' in schema:
            maximum = schema['maximum']
        random_length = random.randint(minimum, maximum)
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random_length))

    elif schema['type'] == 'integer':
        minimum = -10000
        maxmimum = 10000
        if 'minimum' in schema:
            minimum = schema['minimum']
        if 'maximum' in schema:
            maxmimum = schema['maximum']
        return random.randint(minimum, maxmimum)

    elif schema['type'] == 'number':
        minimum = -10000
        maxmimum = 10000
        if 'minimum' in schema:
            minimum = schema['minimum']
        if 'maximum' in schema:
            maxmimum = schema['maximum']
        return round(random.uniform(minimum, maxmimum), 2)

    elif schema['type'] == 'boolean':
        return random.choice([True, False])

    elif schema['type'] == 'object':
        return {prop: generate_random_value(prop_schema) for prop, prop_schema in schema.get('properties', {}).items()}

    elif schema['type'] == 'array':
        if 'items' in schema:
            return [generate_random_value(schema['items'])]

    return None


def send_request(op_id, values):
    url = base_url + operations[op_id]['path']
    headers = [{'Content-Type': 'application/x-www-form-urlencoded'}, {'Content-Type': 'application/json'}, {'Content-Type': 'multipart/form-data'}]
    method = operations[op_id]['method'].lower()
    form_data = {}

    for param in values:
        param_detail = operations[op_id]['parameters'][param]

        if param_detail['in'] == 'body':
            if param == "body":
                form_data = values[param]
            else:
                form_data[param] = values[param]
        elif param_detail['in'] == 'path':
            value = values[param]
            if isinstance(value, list):
                value = random.choice(value)
            url = url.replace('{' + param + '}', str(value))
        elif param_detail['in'] == 'query':
            value = values[param]
            if isinstance(value, list):
                value = random.choice(value)
            if '?' in url:
                url = url + "&" + param + '=' + str(value)
            else:
                url = url + "?" + param + '=' + str(value)
        else:
            print("HEY!!")
            print(param_detail)
            print(param)
            print(op_id)

    try:
        res = requests.request(method, url, headers=headers[0], data=form_data, allow_redirects=False)
    except Exception:
        try:
            res = requests.request(method, url, headers=headers[1], json=form_data, allow_redirects=False)
        except Exception:
            try:
                res = requests.request(method, url, headers=headers[1], data=form_data, allow_redirects=False)
            except Exception:
                res = requests.request(method, url, headers=headers[2], data=form_data, allow_redirects=False)

    return res

def send_mutated_request(op_id, values):
    url = base_url + operations[op_id]['path']
    _url = url
    headers = random.choice([{'Content-Type': 'application/x-www-form-urlencoded'}, {'Content-Type': 'application/json'}, {'Content-Type': 'multipart/form-data'}])

    method = operations[op_id]['method'].lower()
    if random.uniform(0, 1) < 0.2:
        _method = random.choice(["get", "post", "put", "patch", "options", "trace", "head", "delete"])
    form_data = {}
    _values = copy.deepcopy(values)

    for param in _values:
        if random.uniform(0, 1) < 0.2:
            _values[param] = random.choice(["", None, [], {}, "string", "string~!!!@#$^&**()_+", 1, 1.1, "5%", "1970-01-01T00:00:00Z", "1970-01-01", True, 9999999999999999999999999999999999999999999999999999999999999999, 9.999999999999999999999999999999999999999999999999999999999999999])
        param_detail = copy.deepcopy(operations[op_id]['parameters'][param])
        if random.uniform(0, 1) < 0.2:
            param_detail['in'] = random.choice(["body", "in", "query", "path"])
        if param_detail['in'] == 'body':
            if param == "body":
                form_data = _values[param]
            else:
                form_data[param] = _values[param]
        elif param_detail['in'] == 'path':
            value = _values[param]
            if isinstance(value, list) and value:
                value = random.choice(value)
            url = url.replace('{' + param + '}', str(value))
        elif param_detail['in'] == 'query':
            value = _values[param]
            if isinstance(value, list) and value:
                value = random.choice(value)
            if '?' in url:
                url = url + "&" + param + '=' + str(value)
            else:
                url = url + "?" + param + '=' + str(value)

    try:
        res = requests.request(method, url, headers=headers, data=form_data, allow_redirects=False)
    except Exception:
        try:
            res = requests.request(method, url, headers=headers, json=form_data, allow_redirects=False)
        except Exception:
            res = requests.request(method, url, headers=headers, data=form_data, allow_redirects=False)

    return res


def send_required(op_id):
    request_values = {}
    for param in operations[op_id]['parameters']:
        if param in created_resources_op_id and created_resources_op_id[param] != op_id:
            send_required(created_resources_op_id[param])
        target_param = operations[op_id]['parameters'][param]
        if "required" in target_param and target_param["required"]:
            if "enum" in target_param:
                request_values[param] = random.choice(target_param["enum"])
            elif "schema" in target_param and "enum" in target_param["schema"]:
                request_values[param] = random.choice(target_param["schema"]["enum"])
            elif "example" in target_param:
                request_values[param] = target_param["example"]
            elif "schema" in target_param and "example" in target_param["schema"]:
                request_values[param] = target_param["schema"]["example"]
            elif param in inputs:
                request_values[param] = inputs[param][-1]
            elif param in outputs:
                request_values[param] = outputs[param][-1]
            else:
                if "schema" in target_param:
                    request_values[param] = generate_random_value(target_param["schema"])
                else:
                    request_values[param] = generate_random_value(target_param)
    response = send_request(op_id, request_values)
    send_mutated_request(op_id, request_values)
    status_code = response.status_code
    if status_code != 204 and 200 <= status_code < 300:
        if operations[op_id]['method'].lower() == "post":
            for param in request_values:
                if param not in created_resources_op_id:
                    created_resources_op_id[param] = op_id

        for param in request_values:
            if param in inputs:
                inputs[param].append(request_values[param])
            else:
                inputs[param] = [request_values[param]]
        try:
            output = json.loads(response.text)
            update_outputs(output)
        except Exception:
            pass

    return response


def analyze_server_msg(op_id, response):
    _response = []
    http_method = operations[op_id]['method']
    endpoint = base_url + operations[op_id]['path']
    prompt = f"I made a failed request to a REST API endpoint '{http_method} {endpoint}' and received an error response. Here are the request details and the server's response:\n"
    prompt += f"Operation Description: {operations[op_id]['description']}"
    prompt += f"Parameters: {json.dumps(operations[op_id]['parameters'], indent=2)}\n"
    prompt += f"Error Code: {response[0].status_code}\nTried parameter and value: {response[1]}\nResponse Text: {response[0].text}\n"
    prompt += "Based on this information, please identify any potential dependencies among the parameters and suggest valid values for the required parameters. "
    prompt += "Present your suggestions in a structured JSON format without any detail, for example: {'dependencies': [['param1', 'param2'], ['param3', 'param4']], 'values': {'param1': ['value1', 'value2'], 'param2': ['value3', 'value4']}}.\n"

    # Ask ChatGPT for valid values
    valid_values_suggestions = call_chatgpt(prompt)
    try:
        ans = valid_values_suggestions['choices'][0].message.content.strip()

        start_index = ans.find('{')
        end_index = ans.rfind('}') + 1
        json_string = ans[start_index:end_index]
        answer = json.loads(json_string.replace("'", "\""))
    except json.JSONDecodeError:
        answer = None

    if answer:
        if answer["dependencies"]:
            for dep in answer["dependencies"]:
                for _param in dep:
                    if _param in answer["values"]:
                        _res = send_required_llm(op_id, required={_param: answer["values"][_param]}, ipd_check=False)
                        _response.append([_res, {_param: answer["values"][_param]}])
                        if 200 <= _res.status_code < 300:
                            gpt_spec[op_id]["IPD"].append(_param)
                    else:
                        _res = send_required_llm(op_id, required={_param: None}, ipd_check=False)
                        _response.append([_res, {_param: None}])
                        if 200 <= _res.status_code < 300:
                            gpt_spec[op_id]["IPD"].append(_param)
        if answer["values"]:
            _object = {}
            for _param in answer["values"]:
                if _param in operations[op_id]['parameters']:
                    _res = send_required_llm(op_id, required={_param: answer["values"][_param]}, ipd_check=False)
                    _response.append([_res, {_param: answer["values"][_param]}])
                    if 200 <= _res.status_code < 300:
                        gpt_spec[op_id]["IPD"].append(_param)
                else:
                    _object[_param] = answer["values"][_param]
            if _object:
                _res = send_required_llm(op_id, required={"body": _object}, ipd_check=False)
                _response.append([_res, {"body": _object}])
                if 200 <= _res.status_code < 300:
                    gpt_spec[op_id]["IPD"].append("body")

    for _res in _response:
        if 200 <= _res[0].status_code < 300:
            return None
    if _response:
        return random.choice(_response)
    else:
        return response


def send_optional(op_id, required={}, required_params=[], resource=False):
    request_values = {}
    if not required_params:
        ipd = []
        for param in gpt_spec[op_id]['parameters']:
            target_param = gpt_spec[op_id]['parameters'][param]
            if "IPD" in target_param and target_param["IPD"]:
                ipd += target_param["IPD"]

        for _rule in ipd:
            if "Or" in _rule or "OnlyOne" in _rule or "ZeroOrOne" in _rule or "AllOrNone" in _rule:
                param1 = _rule[_rule.find('(') + 1:_rule.find(',')]
                param2 = _rule[_rule.find(',') + 2:_rule.find(')')]
                required_params.append({param1: None, param2: None})
            elif "REQUIRED:" in _rule:
                param1 = _rule[_rule.find(': ') + 2:_rule.find(',')]
                param2 = _rule[_rule.find(', ') + 2:]
                required_params.append({param1: None, param2: None})
            elif "IF " in _rule:
                param1 = _rule[_rule.find('IF ') + 3:_rule.find(' THEN')]
                param2 = _rule[_rule.find('THEN ') + 5:]
                if ";" == param2[-1]:
                    param2 = param2[:-1]
                value1 = None
                value2 = None
                if "==" in param1:
                    value1 = param1[param1.find("'") + 1:param1.rfind("'")]
                    param1 = param1[:param1.find("==")]
                if "==" in param2:
                    value2 = param2[param2.find("'") + 1:param2.rfind("'")]
                    param2 = param2[:param2.find("==")]
                required_params.append({param1: value1, param2: value2})
            else:
                required_params.append({_rule: None})
        for req in required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)
            for j in range(100):
                temp = copy.deepcopy(req)
                for _param in req_params:
                    temp[_param] = None
                random_length = random.randint(0, len(parameters))
                random_key = random.choices(parameters, k=random_length)
                for _param in random_key:
                    if _param not in temp:
                        temp[_param] = None
                send_optional(op_id, temp)
        if not required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)
            for j in range(100):
                temp = {}
                for _param in req_params:
                    temp[_param] = None
                random_length = random.randint(0, len(parameters))
                random_key = random.choices(parameters, k=random_length)
                for _param in random_key:
                    if _param not in temp:
                        temp[_param] = None

                send_optional(op_id, temp, True)

    for _param1 in required:
        if _param1 in created_resources_op_id and created_resources_op_id[_param1] != op_id and not resource:
            send_required_llm(created_resources_op_id[_param1], resource=True)
        if _param1 not in gpt_spec[op_id]['parameters']:
            continue
        target_param = gpt_spec[op_id]['parameters'][_param1]
        if "schema" in target_param:
            param_type = target_param["schema"]["type"]
        else:
            param_type = target_param["type"]

        if ("required" in target_param and target_param["required"]) or _param1 in required:
            if _param1 in required and required[_param1]:
                if isinstance(required[_param1], list):
                    if param_type == "array":
                        request_values[_param1] = required[_param1]
                    else:
                        request_values[_param1] = random.choice(required[_param1])
                else:
                    request_values[_param1] = required[_param1]
            elif "enum" in target_param:
                request_values[_param1] = random.choice(target_param["enum"])
            elif "schema" in target_param and "enum" in target_param["schema"]:
                request_values[_param1] = random.choice(target_param["schema"]["enum"])
            elif "examples" in target_param and target_param["examples"] != ["None"] and target_param["examples"]:
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["examples"], num_to_select)
                    request_values[_param1] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for __param in target_param["examples"]:
                        if target_param["schema"]["properties"][__param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["examples"][__param], num_to_select)
                            _object[__param] = selected_elements
                        else:
                            if target_param["examples"][__param]:
                                _object[__param] = random.choice(target_param["examples"][__param])
                    request_values[_param1] = _object
                else:
                    request_values[_param1] = random.choice(target_param["examples"])
            elif "generated" in target_param and target_param["generated"] != ["None"] and target_param["generated"]:
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["generated"], num_to_select)
                    request_values[_param1] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for __param in target_param["generated"]:
                        if target_param["schema"]["properties"][__param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["generated"][__param], num_to_select)
                            _object[__param] = selected_elements
                        else:
                            _object[__param] = random.choice(target_param["generated"][__param])
                    request_values[_param1] = _object
                else:
                    request_values[_param1] = random.choice(target_param["generated"])
            elif "example" in target_param:
                request_values[_param1] = target_param["example"]
            elif _param1 in inputs:
                request_values[_param1] = inputs[_param1][-1]
            elif _param1 in outputs:
                request_values[_param1] = outputs[_param1][-1]
            else:
                if "schema" in target_param:
                    request_values[_param1] = generate_random_value(target_param["schema"])
                else:
                    request_values[_param1] = generate_random_value(target_param)

    response = send_request(op_id, request_values)
    send_mutated_request(op_id, request_values)
    status_code = response.status_code

    if status_code != 204 and 200 <= status_code < 300:
        if operations[op_id]['method'].lower() == "post":
            for param in request_values:
                if param not in created_resources_op_id:
                    created_resources_op_id[param] = op_id

        for param in request_values:
            if param in inputs:
                inputs[param].append(request_values[param])
            else:
                inputs[param] = [request_values[param]]
        try:
            output = json.loads(response.text)
            update_outputs(output)
        except Exception:
            pass


def send_optional_llm(op_id, required={}, required_params=[], resource=False):
    request_values = {}
    if not required_params:
        ipd = []
        for param in gpt_spec[op_id]['parameters']:
            target_param = gpt_spec[op_id]['parameters'][param]
            if "IPD" in target_param and target_param["IPD"]:
                ipd += target_param["IPD"]

        for _rule in ipd:
            if "Or" in _rule or "OnlyOne" in _rule or "ZeroOrOne" in _rule or "AllOrNone" in _rule:
                param1 = _rule[_rule.find('(') + 1:_rule.find(',')]
                param2 = _rule[_rule.find(',') + 2:_rule.find(')')]
                required_params.append({param1: None, param2: None})
            elif "REQUIRED:" in _rule:
                param1 = _rule[_rule.find(': ') + 2:_rule.find(',')]
                param2 = _rule[_rule.find(', ') + 2:]
                required_params.append({param1: None, param2: None})
            elif "IF " in _rule:
                param1 = _rule[_rule.find('IF ') + 3:_rule.find(' THEN')]
                param2 = _rule[_rule.find('THEN ') + 5:]
                if ";" == param2[-1]:
                    param2 = param2[:-1]
                value1 = None
                value2 = None
                if "==" in param1:
                    value1 = param1[param1.find("'") + 1:param1.rfind("'")]
                    param1 = param1[:param1.find("==")]
                if "==" in param2:
                    value2 = param2[param2.find("'") + 1:param2.rfind("'")]
                    param2 = param2[:param2.find("==")]
                required_params.append({param1: value1, param2: value2})
            else:
                required_params.append({_rule: None})
        for req in required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)

            temp = copy.deepcopy(req)
            for _param in req_params:
                temp[_param] = None
            random_length = random.randint(0, len(parameters))
            random_key = random.choices(parameters, k=random_length)
            for _param in random_key:
                if _param not in temp:
                    temp[_param] = None
            send_optional_llm(op_id, temp)
        if not required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)
            for j in range(100):
                temp = {}
                for _param in req_params:
                    temp[_param] = None
                random_length = random.randint(0, len(parameters))
                random_key = random.choices(parameters, k=random_length)
                for _param in random_key:
                    if _param not in temp:
                        temp[_param] = None

                send_optional_llm(op_id, temp, True)

    for _param1 in required:
        if _param1 in created_resources_op_id and created_resources_op_id[_param1] != op_id and not resource:
            send_required_llm(created_resources_op_id[_param1], resource=True)
        if _param1 not in gpt_spec[op_id]['parameters']:
            continue
        target_param = gpt_spec[op_id]['parameters'][_param1]
        if "schema" in target_param:
            param_type = target_param["schema"]["type"]
        else:
            param_type = target_param["type"]

        if ("required" in target_param and target_param["required"]) or _param1 in required:
            if _param1 in required and required[_param1]:
                if isinstance(required[_param1], list):
                    if param_type == "array":
                        request_values[_param1] = required[_param1]
                    else:
                        request_values[_param1] = random.choice(required[_param1])
                else:
                    request_values[_param1] = required[_param1]
            elif "enum" in target_param:
                request_values[_param1] = random.choice(target_param["enum"])
            elif "schema" in target_param and "enum" in target_param["schema"]:
                request_values[_param1] = random.choice(target_param["schema"]["enum"])
            elif "examples" in target_param and target_param["examples"] != ["None"] and target_param["examples"]:
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["examples"], num_to_select)
                    request_values[_param1] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for __param in target_param["examples"]:
                        if target_param["schema"]["properties"][__param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["examples"][__param], num_to_select)
                            _object[__param] = selected_elements
                        else:
                            if target_param["examples"][__param]:
                                _object[__param] = random.choice(target_param["examples"][__param])
                    request_values[_param1] = _object
                else:
                    request_values[_param1] = random.choice(target_param["examples"])
            elif "generated" in target_param and target_param["generated"] != ["None"] and target_param["generated"]:
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["generated"], num_to_select)
                    request_values[_param1] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for __param in target_param["generated"]:
                        if target_param["schema"]["properties"][__param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["generated"][__param], num_to_select)
                            _object[__param] = selected_elements
                        else:
                            _object[__param] = random.choice(target_param["generated"][__param])
                    request_values[_param1] = _object
                else:
                    request_values[_param1] = random.choice(target_param["generated"])
            elif "example" in target_param:
                request_values[_param1] = target_param["example"]
            elif _param1 in inputs:
                request_values[_param1] = inputs[_param1][-1]
            elif _param1 in outputs:
                request_values[_param1] = outputs[_param1][-1]
            else:
                if "schema" in target_param:
                    request_values[_param1] = generate_random_value(target_param["schema"])
                else:
                    request_values[_param1] = generate_random_value(target_param)

    response = send_request(op_id, request_values)
    send_mutated_request(op_id, request_values)
    status_code = response.status_code

    if status_code != 204 and 200 <= status_code < 300:
        if operations[op_id]['method'].lower() == "post":
            for param in request_values:
                if param not in created_resources_op_id:
                    created_resources_op_id[param] = op_id

        for param in request_values:
            if param in inputs:
                inputs[param].append(request_values[param])
            else:
                inputs[param] = [request_values[param]]
        try:
            output = json.loads(response.text)
            update_outputs(output)
        except Exception:
            pass

    if status_code >= 400:
        attempt = 0
        _response = [response, request_values]
        while status_code >= 400 and attempt < 5:
            attempt += 1

            _response = analyze_server_msg(op_id, _response)
            if _response is None:
                break
            status_code = _response[0].status_code


def send_all(op_id, required={}, required_params=[], resource=False):
    request_values = {}

    if not required_params:
        ipd = []
        for param in gpt_spec[op_id]['parameters']:
            target_param = gpt_spec[op_id]['parameters'][param]
            if "IPD" in target_param and target_param["IPD"]:
                ipd += target_param["IPD"]

        for _rule in ipd:
            if "Or" in _rule or "OnlyOne" in _rule or "ZeroOrOne" in _rule or "AllOrNone" in _rule:
                param1 = _rule[_rule.find('(') + 1:_rule.find(',')]
                param2 = _rule[_rule.find(',') + 2:_rule.find(')')]
                required_params.append({param1: None, param2: None})
            elif "REQUIRED:" in _rule:
                param1 = _rule[_rule.find(': ') + 2:_rule.find(',')]
                param2 = _rule[_rule.find(', ') + 2:]
                required_params.append({param1: None, param2: None})
            elif "IF " in _rule:
                param1 = _rule[_rule.find('IF ') + 3:_rule.find(' THEN')]
                param2 = _rule[_rule.find('THEN ') + 5:]
                if ";" == param2[-1]:
                    param2 = param2[:-1]
                value1 = None
                value2 = None
                if "==" in param1:
                    value1 = param1[param1.find("'") + 1:param1.rfind("'")]
                    param1 = param1[:param1.find("==")]
                if "==" in param2:
                    value2 = param2[param2.find("'") + 1:param2.rfind("'")]
                    param2 = param2[:param2.find("==")]
                required_params.append({param1: value1, param2: value2})
            else:
                required_params.append({_rule: None})
        for req in required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)
            for j in range(1000):
                temp = copy.deepcopy(req)
                for _param in req_params:
                    temp[_param] = None
                random_length = random.randint(0, len(parameters))
                random_key = random.choices(parameters, k=random_length)
                for _param in random_key:
                    if _param not in temp:
                        temp[_param] = None

                send_optional(op_id, temp)
        if not required_params:
            parameters = list(gpt_spec[op_id]['parameters'].keys())
            req_params = []
            for _param in gpt_spec[op_id]['parameters']:
                temp_param = gpt_spec[op_id]['parameters'][_param]
                # Required parameter should be processed1
                if "required" in temp_param and temp_param["required"]:
                    req_params.append(_param)
            for j in range(1000):
                temp = {}
                for _param in req_params:
                    temp[_param] = None
                random_length = random.randint(0, len(parameters))
                random_key = random.choices(parameters, k=random_length)
                for _param in random_key:
                    if _param not in temp:
                        temp[_param] = None

                send_optional(op_id, temp, True)

    for _param1 in required:
        if _param1 in created_resources_op_id and created_resources_op_id[_param1] != op_id and not resource:
            send_required_llm(created_resources_op_id[_param1], resource=True)
        if _param1 not in gpt_spec[op_id]['parameters']:
            continue
        target_param = gpt_spec[op_id]['parameters'][_param1]
        if "schema" in target_param:
            param_type = target_param["schema"]["type"]
        else:
            param_type = target_param["type"]

        if ("required" in target_param and target_param["required"]) or _param1 in required:
            value = None
            choice = random.choice([1,2,3,4,5,6,7])
            if choice == 1:
                if _param1 in required and required[_param1]:
                    if isinstance(required[_param1], list):
                        if param_type == "array":
                            request_values[_param1] = required[_param1]
                        else:
                            request_values[_param1] = random.choice(required[_param1])
                    else:
                        request_values[_param1] = required[_param1]
            elif choice == 2:
                if "enum" in target_param:
                    request_values[_param1] = random.choice(target_param["enum"])
                elif "schema" in target_param and "enum" in target_param["schema"]:
                    request_values[_param1] = random.choice(target_param["schema"]["enum"])
            elif choice == 3:
                if "examples" in target_param and target_param["examples"] != ["None"] and target_param["examples"]:
                    if param_type == "array":
                        num_to_select = random.randint(1, len(target_param["examples"]))
                        selected_elements = random.sample(target_param["examples"], num_to_select)
                        request_values[_param1] = selected_elements
                    elif param_type == "object":
                        _object = {}
                        for __param in target_param["examples"]:
                            if target_param["schema"]["properties"][__param]["type"] == "array":
                                num_to_select = random.randint(1, len(target_param["examples"][_param]))
                                selected_elements = random.sample(target_param["examples"][__param], num_to_select)
                                _object[__param] = selected_elements
                            else:
                                if target_param["examples"][__param]:
                                    _object[__param] = random.choice(target_param["examples"][__param])
                        request_values[_param1] = _object
                    else:
                        request_values[_param1] = random.choice(target_param["examples"])
            elif choice == 4:
                if "generated" in target_param and target_param["generated"] != ["None"] and target_param["generated"]:
                    if param_type == "array":
                        num_to_select = random.randint(1, len(target_param["examples"]))
                        selected_elements = random.sample(target_param["generated"], num_to_select)
                        request_values[_param1] = selected_elements
                    elif param_type == "object":
                        _object = {}
                        for __param in target_param["generated"]:
                            if target_param["schema"]["properties"][__param]["type"] == "array":
                                num_to_select = random.randint(1, len(target_param["examples"][_param]))
                                selected_elements = random.sample(target_param["generated"][__param], num_to_select)
                                _object[__param] = selected_elements
                            else:
                                _object[__param] = random.choice(target_param["generated"][__param])
                        request_values[_param1] = _object
                    else:
                        request_values[_param1] = random.choice(target_param["generated"])
            elif choice == 5:
                if "example" in target_param:
                    request_values[_param1] = target_param["example"]
            elif choice == 6:
                if _param1 in inputs:
                    request_values[_param1] = inputs[_param1][-1]
            elif choice == 7:
                if _param1 in outputs:
                    request_values[_param1] = outputs[_param1][-1]
            if value is None:
                if "schema" in target_param:
                    request_values[_param1] = generate_random_value(target_param["schema"])
                else:
                    request_values[_param1] = generate_random_value(target_param)

            request_values[_param1] = value

    response = send_request(op_id, request_values)
    send_mutated_request(op_id, request_values)
    status_code = response.status_code

    if status_code != 204 and 200 <= status_code < 300:
        if operations[op_id]['method'].lower() == "post":
            for param in request_values:
                if param not in created_resources_op_id:
                    created_resources_op_id[param] = op_id

        for param in request_values:
            if param in inputs:
                inputs[param].append(request_values[param])
            else:
                inputs[param] = [request_values[param]]
        try:
            output = json.loads(response.text)
            update_outputs(output)
        except Exception:
            pass

def send_required_llm(op_id, ipd=None, ipd_check=True, resource=False, required={}):
    request_values = {}
    if not ipd:
        ipd = []
    if op_id not in gpt_spec:
        return None
    for param in gpt_spec[op_id]['parameters']:
        if param in created_resources_op_id and created_resources_op_id[param] != op_id and not resource:
            send_required_llm(created_resources_op_id[param], resource=True)
        target_param = gpt_spec[op_id]['parameters'][param]
        if "schema" in target_param:
            param_type = target_param["schema"]["type"]
        else:
            param_type = target_param["type"]
        if "IPD" in target_param and target_param["IPD"]:
            ipd += target_param["IPD"]
        if ("required" in target_param and target_param["required"]) or param in required:
            if param in required and required[param]:
                if isinstance(required[param], list):
                    if param_type == "array":
                        request_values[param] = required[param]
                    else:
                        request_values[param] = random.choice(required[param])
                else:
                    request_values[param] = required[param]
            elif "enum" in target_param:
                request_values[param] = random.choice(target_param["enum"])
            elif "schema" in target_param and "enum" in target_param["schema"]:
                request_values[param] = random.choice(target_param["schema"]["enum"])
            elif "examples" in target_param and target_param["examples"] != ["None"] and target_param["examples"]:
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["examples"], num_to_select)
                    request_values[param] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for _param in target_param["examples"]:
                        if target_param["schema"]["properties"][_param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["examples"][_param], num_to_select)
                            _object[_param] = selected_elements
                        else:
                            if target_param["examples"][_param]:
                                _object[_param] = random.choice(target_param["examples"][_param])
                    request_values[param] = _object
                else:
                    request_values[param] = random.choice(target_param["examples"])
            elif "generated" in target_param and target_param["generated"] != ["None"] and target_param["generated"]:
                if "schema" in target_param:
                    param_type = target_param["schema"]["type"]
                else:
                    param_type = target_param["type"]
                if param_type == "array":
                    num_to_select = 1 #random.randint(1, len(target_param["examples"]))
                    selected_elements = random.sample(target_param["generated"], num_to_select)
                    request_values[param] = selected_elements
                elif param_type == "object":
                    _object = {}
                    for _param in target_param["generated"]:
                        if target_param["schema"]["properties"][_param]["type"] == "array":
                            num_to_select = 1 #random.randint(1, len(target_param["examples"][_param]))
                            selected_elements = random.sample(target_param["generated"][_param], num_to_select)
                            _object[_param] = selected_elements
                        else:
                            _object[_param] = random.choice(target_param["generated"][_param])
                    request_values[param] = _object
                else:
                    request_values[param] = random.choice(target_param["generated"])
            elif "example" in target_param:
                request_values[param] = target_param["example"]
            elif param in inputs:
                request_values[param] = inputs[param][-1]
            elif param in outputs:
                request_values[param] = outputs[param][-1]
            else:
                if "schema" in target_param:
                    request_values[param] = generate_random_value(target_param["schema"])
                else:
                    request_values[param] = generate_random_value(target_param)

    response = send_request(op_id, request_values)
    send_mutated_request(op_id, request_values)
    status_code = response.status_code

    if status_code != 204 and 200 <= status_code < 300:
        if operations[op_id]['method'].lower() == "post":
            for param in request_values:
                if param not in created_resources_op_id:
                    created_resources_op_id[param] = op_id

        for param in request_values:
            if param in inputs:
                inputs[param].append(request_values[param])
            else:
                inputs[param] = [request_values[param]]
        try:
            output = json.loads(response.text)
            update_outputs(output)
        except Exception:
            pass

    if ipd_check:
        if status_code >= 400:
            attempt = 0
            _response = [response, request_values]
            while status_code >= 400 and attempt < 5:
                attempt += 1

                _response = analyze_server_msg(op_id, _response)
                if _response is None:
                    break
                status_code = _response[0].status_code
        for _rule in ipd:
            if "Or" in _rule or "OnlyOne" in _rule or "ZeroOrOne" in _rule or "AllOrNone" in _rule:
                param1 = _rule[_rule.find('(')+1:_rule.find(',')]
                param2 = _rule[_rule.find(',')+2:_rule.find(')')]
                send_required_llm(op_id, required={param1:None}, ipd_check=False)
                send_required_llm(op_id, required={param2:None}, ipd_check=False)
            elif "REQUIRED:" in _rule:
                param1 = _rule[_rule.find(': ') + 2:_rule.find(',')]
                param2 = _rule[_rule.find(', ') + 2:]
                send_required_llm(op_id, required={param1: None}, ipd_check=False)
                send_required_llm(op_id, required={param2: None}, ipd_check=False)
            elif "IF " in _rule:
                param1 = _rule[_rule.find('IF ') + 3:_rule.find(' THEN')]
                param2 = _rule[_rule.find('THEN ') + 5:]
                if ";" == param2[-1]:
                    param2 = param2[:-1]
                value1 = None
                value2 = None
                if "==" in param1:
                    value1 = param1[param1.find("'")+1:param1.rfind("'")]
                    param1 = param1[:param1.find("==")]
                if "==" in param2:
                    value2 = param2[param2.find("'")+1:param2.rfind("'")]
                    param2 = param2[:param2.find("==")]
                send_required_llm(op_id, required={param1: value1, param2: value2}, ipd_check=False)
            else:
                send_required_llm(op_id, required={_rule: None}, ipd_check=False)

    return response


def update_outputs(d, parent_key='', leaf_properties=None):
    if leaf_properties is None:
        leaf_properties = {}

    for key, value in d.items():
        new_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            update_outputs(value, new_key, leaf_properties)
        elif isinstance(value, list):
            for val in value:
                update_outputs(val, new_key, leaf_properties)
        elif value:
            if new_key in outputs:
                outputs[new_key].append(value)
            else:
                outputs[new_key] = [value]

    return leaf_properties


if __name__ == '__main__':
    openapi_spec_file = "../../../specs/openapi/genome-nexus.yaml"
    restgpt_file = "../../../restgpt/genome-nexus.json"
    openai_api_key = "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"
    openapi_spec = prance.ResolvingParser(openapi_spec_file, strict=False).specification
    base_url = openapi_spec['servers'][0]['url']
    if base_url[-1] == '/':
        base_url = base_url[:-1]

    op_id_list = []
    operations = {}
    parse_oas(openapi_spec)
    test_sequence = []
    if 1 < len(op_id_list) < 30:
        for i in range(5):
            test_sequence = generate_operation_sequence()
            for seq in test_sequence:
                if seq not in op_id_list:
                    continue
            break
    else:
        test_sequence = op_id_list

    created_resources_op_id = {}
    inputs = {}
    outputs = {}
    for sequence in test_sequence:
        response = send_required(sequence)

    gpt_spec = copy.deepcopy(operations)
    with open(restgpt_file, 'r') as file:
        restgpt = json.load(file)
    for op_id in operations:
        gpt_spec[op_id]["IPD"] = []
        path = operations[op_id]['path']
        method = operations[op_id]['method']
        for param in operations[op_id]['parameters']:
            gpt_spec[op_id]["parameters"][param]["examples"] = []
            gpt_spec[op_id]["parameters"][param]["generated"] = []
            gpt_spec[op_id]["parameters"][param]["IPD"] = []

    for sequence in test_sequence:
        send_required_llm(sequence)

    for sequence in test_sequence:
        send_optional(sequence)

    for sequence in test_sequence:
        send_optional_llm(sequence)

    for sequence in test_sequence:
        send_all(sequence)