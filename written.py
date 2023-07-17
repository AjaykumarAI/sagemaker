from collections import defaultdict

def xtract_written_line(text, text_new, reference_dict, writ_line_list):
    date_pattern = "(0[1-9]|[1-2]?[0-9]|3[01])\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(19[0-9]{2}|[2-9][0-9]{3})"
    written_line_dict = {}
    written_date_dict = {}
    risk_code_dict = {}
    entity_dict = {}
    entity_list = ['510', '1880', '5307', '5332']
    risk_code_list = []
    orig_text = text
    tokio_dict = {'tokio': [], 'KLN': []}
    stamp_dict = defaultdict(list)
    text_list = text.lower().split()

    # written_date regex
    for date_match in re.finditer(date_pattern, text, re.I):
        modified_text = text.replace(date_match.group(), "dateextracted")
        modified_text_list = modified_text.split()
        date_idx_list = []
        for idx, word in enumerate(modified_text_list):
            if word == "dateextracted":
                date_idx_list.append(idx)
        written_date_dict[date_match.group()] = date_idx_list

    # risk code
    text_new_list = text_new.split("\n")
    for idx, word in enumerate(text_new_list):
        if re.search("Risk Code", word):
            risk_code_list.append(text_new_list[idx + 1])
        if re.search("Description", word):
            pot_risk_code = text_new_list[idx + 1].split()
            for i in pot_risk_code:
                if i in master_risk_code_list:
                    risk_code_list.append(i)

    i = 0
    for idx, word in enumerate(text_list):
        if word == "written":
            if text_list[idx + 1] == "line":
                text = "".join(text_list[idx + 2:idx + 4])
                writ_line_ = re.search("(\d*(\.\d+)?%)", text)
                if writ_line_:
                    written_line_dict[idx + 2] = writ_line_.group()
        if word in writ_line_list:
            written_line_dict[idx] = word

        if word == "risk":
            if re.search("code", text_list[idx + 1]):
                if i < len(risk_code_list):
                    if risk_code_list[i] not in risk_code_dict:
                        risk_code_dict[risk_code_list[i]] = [idx + 2]
                    else:
                        risk_code_dict[risk_code_list[i]].append(idx + 2)

        if word.strip(":").strip(".").strip() == "description":
            if i < len(risk_code_list):
                if risk_code_list[i] not in risk_code_dict:
                    risk_code_dict[risk_code_list[i]] = [idx + 1]
                else:
                    risk_code_dict[risk_code_list[i]].append(idx + 1)

                i += 1

        if word == "tokio":
            tokio_dict['tokio'].append(idx)
        elif word.upper() == "KLN":
            tokio_dict['KLN'].append(idx)

        if word == "lloyd's":
            if text_list[idx + 1] == "stamp:":
                if "510/1880" in text_list[idx + 2]:
                    stamp_dict[text_list[idx + 2]].append(idx + 2)
                elif "510" in text_list[idx + 2]:
                    stamp_dict[text_list[idx + 2]].append(idx + 2)
                elif "1880" in text_list[idx + 2]:
                    stamp_dict[text_list[idx + 2]].append(idx + 2)
                elif "5307" in text_list[idx + 2]:
                    stamp_dict[text_list[idx + 2]].append(idx + 2)
                elif "5332" in text_list[idx + 2]:
                    stamp_dict[text_list[idx + 2]].append(idx + 2)
            elif re.search("written", text_list[idx + 1]) and re.search("line", text_list[idx + 2]):
                writ_line_ = re.search("(\d*(\.\d+)?%)", text_list[idx + 3])
                if writ_line_:
                    written_line_dict[idx + 3] = writ_line_.group()

    for idx, word in enumerate(text_list):
        if word == "lic:":
            stamp_dict[text_list[idx + 1]].append(idx + 1)
        if word == "lloyds:":
            stamp_dict[text_list[idx + 1]].append(idx + 1)

    if len(tokio_dict['tokio']) > 0:
        tokio_list = tokio_dict['tokio']
    elif len(tokio_dict['KLN']) > 0:
        tokio_list = tokio_dict['KLN']
    else:
        tokio_list = []

    written_line = ""
    written_date = ""
    risk_code = ""
    risk_code_index = list(risk_code_dict.keys())
    written_line_index = list(written_line_dict.keys())
    written_date_index = []

    for date, idx_value in written_date_dict.items():
        written_date_index.extend(idx_value)

    try:
        written_date_idx, min_index = min_diff(tokio_list, written_date_index)
        for key, val in written_date_dict.items():
            if written_date_idx in val:
                written_date = key
                break
    except:
        pass

    text = orig_text.replace("510", " 510 ").replace("1880", " 1880 ").replace("5307", " 5307 ").replace("5332", " 5332 ")

    for entity in entity_list:
        index_list = []
        text_list = text.split()
        if entity in text:
            for idx, word in enumerate(text_list):
                if word == entity:
                    index_list.append(idx)
            entity_dict[entity] = index_list

    return written_line_dict, stamp_dict, tokio_dict, risk_code_dict, written_date, entity_dict
