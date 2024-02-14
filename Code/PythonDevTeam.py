from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager


def generate_python_code(topic):

    config_list = [
        {'model': 'gpt-3.5-turbo',
         'api_key': api},
    ]

    summary_gen_prmpt = "You are an editor for new york times and work for the technical and AI development and advances team. Using the topic provided you are to create an article that will be published in next days newspaper. However, while generating summary also generate places whereever relevant images are to be inserted. These placeholders can be identified with a tag <Image Here : Image Summary>. Image summary is a DALLE relevant prompt template to generate the relevant image."

    Emp_Editor = AssistantAgent(name="Emp_Editor"
                                , system_message=summary_gen_prmpt
                                , llm_config={"config_list": config_list}
                                , description = "A sub-editor agent that creates first drafts and futher changes as directed by Editor."
                                )

    summary_val_prmpt = "You are the top editor for new york times and work for the technical and AI development and advances team. Using the summary generated by the sub-editor, you have to redline to generate a perfect article. Make sure there are at little changes highlighted as possible. If you need to highlight the error in article more than once, then you are doing horrible job."

    Boss_Editor = AssistantAgent(name="Boss_Editor"
                                 , system_message=summary_val_prmpt
                                 , llm_config={"config_list": config_list}
                                 , description = "An editor agent that validates and suggests changes to sub-editor."
                                 )

    groupchat = GroupChat(agents=[Emp_Editor, Boss_Editor], messages=[], max_round=4,
                          speaker_selection_method='round_robin')
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

    summary_wri_prmpt = "You are the the digital writer for new york times and work for the technical and AI development and advances team. Using the results generated by final results after from conversation between, convert the article into HTML format. Each paragraph marked by <p></p> tags. Headers with <H3></H3>. Title with <H1></H1>. Keep images in Bold."

    Digital_Writer = AssistantAgent(name="Digital_Writer"
                                    , system_message=summary_wri_prmpt
                                    , llm_config={"config_list": config_list}
                                    , description = "Digital writer that writes the final content in form of HTMl after removing non-relevant texts."
                                    )

    groupchat = GroupChat(agents=[Emp_Editor, Boss_Editor, Digital_Writer], messages=[], max_round=4,
                          speaker_selection_method='auto')
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})



    user_proxy = UserProxyAgent(
        "user_proxy", code_execution_config={"work_dir": "Code",
                                             "use_docker": False}
    )

    user_proxy.initiate_chat(manager,message=topic)

    if len(groupchat.messages[-1]['content'].strip()):
        return groupchat.messages[-1]['content']
    else:
        return groupchat.messages[-2]['content']
