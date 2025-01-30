from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

## setting the environment variables
env_path= r"D:\common_credentials\.env"
load_dotenv(dotenv_path=env_path)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')



#api parameters: https://microsoft.github.io/autogen/0.2/docs/topics/non-openai-models/cloud-togetherai#api-parameters
config_list =[{'model': 'deepseek-r1-distill-llama-70b',
               'api_key': GROQ_API_KEY,
               "api_type": "groq"}]

 ## LLM Config
llm_config = {"config_list": config_list}


# https://microsoft.github.io/autogen/0.2/docs/topics/llm_configuration
deepseek_config = {
    # "cache_seed" : 45,  #to get reproducible results always
    "temperaturre": 0.5,
    "config_list": config_list,
    "timeout": 120
}

task = """
**Task**: As an architect, you are required to design solution for the following business requirement:
    - Data storage for the massive amount of Healthcare IoT data
    - Real time data analytics and scalable machine learning pipeline
    - Scalability
    - Cost Optimization
    - Region pairs in Asia and Europe for disaster recovery
    - Tools for monitoring & obeservability of Machine learning applications
    - Timeline- 6 months
"""

cloud_prompt= """
**Role**: You are a cloud architect at a healthcare company. You are tasked with designing a solution for the following business requirements:
only use open-source frameworks that are popular and have lots of active contributors.
At the end briefly state the advantages of open-source adoption and summarize your solution using table for clarity."""

cloud_prompt= cloud_prompt + task
print(cloud_prompt)

oss_prompt = """
**Role**: You are an expert open-source sofware advocate. You need to develop architecture propoesal without considering cloud solutions.
only use open-source frameworks that are popular and have lots of active contributors.
At the end briefly state the advantages of open-source adoption and summarize your solution using table for clarity"""
oss_prompt = oss_prompt + task

print("\n",oss_prompt)

lead_prompt = """
**Role**: You are an expert lead architech tasked with managing a conversation between the cloud and open-source architech. 
Each architech will perform a task and reponds with their results. You will critically review the results and ask for, disadvanatages on their solutions.
You will review each result, and choose the best solution for the company accordance with business requirements and architecure best practice.
You will use any number of summary tables to communicate your decision."""
lead_prompt = lead_prompt + task
print("\n",lead_prompt)

# https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/user_proxy_agent/
user = UserProxyAgent(name="Suprevisor",
                system_message= "A human head of Architecture team",
                code_execution_config= {
                    "last_n_messages": 2,
                    "work_dir": "groupchat",
                    "max_consecutive_auto_reply":2,
                    "use_docker":False,
                    "human_input_mode": "Never"
                                })

#cloud agent
cloud_agent = AssistantAgent(name="Cloud Architech",
                             system_message= cloud_prompt,
                             llm_config= deepseek_config,
                            
                             ) 


#open-source sofware advocate
os_advocate = AssistantAgent(name="open-source sofware advocate",
                             system_message= oss_prompt,
                             llm_config= deepseek_config,
                            
                             ) 


#open-source sofware advocate
lead_architech = AssistantAgent(name="lead architech of team",
                             system_message= lead_prompt,
                             llm_config= deepseek_config,
                            
                             )

# https://microsoft.github.io/autogen/0.2/blog/2024/02/11/FSM-GroupChat/
def state_transition(last_speaker, groupchat):
    ## user >> cloud_agent >> os_advocate >> lead_architech >> None
    if last_speaker is user:
        return cloud_agent
    elif last_speaker is cloud_agent:
        return os_advocate
    elif last_speaker is os_advocate:
        return lead_architech
    elif last_speaker is lead_architech:
        #lead > end
        return None

#Initialize chat
# https://microsoft.github.io/autogen/0.2/docs/notebooks/agentchat_groupchat/
groupchat= GroupChat(
    agents=[user, cloud_agent, os_advocate, lead_architech],
    messages=[],
    max_round=4,
    speaker_selection_method= state_transition   # "auto": the next speaker is selected automatically by LLM. "manual": the next speaker is selected manually by user input."random": the next speaker is selected randomly.
)

#GroupChatManager: A chat manager agent that can manage a group chat of multiple agents.
# https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/#groupchatmanager
manager= GroupChatManager(groupchat=groupchat,
                        llm_config= llm_config)

response = user.initiate_chat(
    manager,
    message= "Provide your best architecture based on these business requirements"
)

#store output in text documents
# with open("groupchat_output.txt", "w") as f:
#     f.write(str(response.chat_history))