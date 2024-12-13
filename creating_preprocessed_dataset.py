import pandas as pd 
import numpy as np
import re 
df = pd.read_json("papers.json")
df.head()
reviews_list = pd.Series()
list_disambiguate = [];
score_disambiguate = [];
conf_disambiguate = [];
accepted_disambiguate = [];
titles_disambiguate = [];
scores_list = pd.Series()
confs_list = pd.Series()
for i in df.index:
    score_list = []
    conf_list = []
    review_list = []
    for rev in df["reviews"][i]:
        text = df["reviews"][i][rev]["comments"]
        if re.search(r"reviewer*", text, re.IGNORECASE):  # Fix later: "this reviewer" and "the reviewer" referring to onesself 
            #breakpoint()
            continue
        if re.search(r"we thank", text, re.IGNORECASE):
            continue
        if len(text) < 300: # must be more than 300 chars
            continue
        score_list.append(df["reviews"][i][rev]["recommendation"])
        conf_list.append(df["reviews"][i][rev]["REVIEWER_CONFIDENCE"])
        review_list.append(text)
        score_disambiguate.append(df["reviews"][i][rev]["recommendation"])
        conf_disambiguate.append(df["reviews"][i][rev]["REVIEWER_CONFIDENCE"])
        list_disambiguate.append(text)
        accepted_disambiguate.append(df["accepted"][i])
        titles_disambiguate.append(df["paper_title"][i])

    score_list = pd.Series(score_list)
    score_list.fillna(np.nan, inplace=True)
    conf_list = pd.Series(conf_list)
    conf_list.fillna(np.nan, inplace=True)
    review_list = pd.Series(review_list)
    if score_list.isna().all():
        scores_list[i] = np.nan
    else:
        scores_list[i] = np.nanmean(score_list)
        #print(i)
    if conf_list.isna().all():
        confs_list[i] = np.nan
    else:
        confs_list[i] = np.nanmean(conf_list)
    if review_list.isna().all():
        reviews_list[i] = ""
    else:
        reviews_list[i] = "".join(review_list)


percent_usable = ((~confs_list.isnull()).sum())/len(confs_list) 
print(percent_usable) 
percent_usable = ((~scores_list.isnull()).sum())/len(confs_list) 
print(percent_usable) 
#breakpoint()
breakpoint()
list_disambiguated = pd.Series(list_disambiguate)
scores_disambiguated = pd.Series(score_disambiguate)
confs_disambiguated = pd.Series(conf_disambiguate)
accepted_disambiguated = pd.Series(accepted_disambiguate)
titles_disambiguated = pd.Series(titles_disambiguate)
df3 = pd.DataFrame(columns=["accepted", "title", "review", "score" "conf_score"])
df3["accepted"] = accepted_disambiguated
df3["title"] = titles_disambiguated
df3["review"] = list_disambiguated
df3["score"] = scores_disambiguated
df3["conf_score"] = confs_disambiguated
df3 = df3.drop(df3[df3["review"]==""].index)
df3.to_csv("data_new_no_thanks_no_reviewers_each_review_separate.csv")