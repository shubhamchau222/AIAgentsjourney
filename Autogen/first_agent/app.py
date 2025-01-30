import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

# Setting environment variables
env_path = r"D:\common_credentials\.env"
load_dotenv(dotenv_path=env_path)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# API parameters
config_list = [{'model': 'deepseek-r1-distill-llama-70b',
                'api_key': GROQ_API_KEY,
                "api_type": "groq"}]

# LLM Config
llm_config = {"config_list": config_list}

# Deepseek config
deepseek_config = {
    "cache_seed": 45,  # to get reproducible results always
    "temperature": 0.5,
    "config_list": config_list,
    "timeout": 120
}

# Function to initialize the chat system
def initialize_agents(task):
    # Prompts for different agents
    cloud_prompt = f"""
    **Role**: You are a cloud architect at a healthcare company. You are tasked with designing a solution for the following business requirements:
    only use open-source frameworks that are popular and have lots of active contributors.
    At the end briefly state the advantages of open-source adoption and summarize your solution using table for clarity.
    {task}
    """

    oss_prompt = f"""
    **Role**: You are an expert open-source software advocate. You need to develop architecture proposals using only open-source frameworks. 
    Always your approch should be based on the popular and active contributors. Try to add on yourself, do not copy the cloud architect.
    {task}
    """

    lead_prompt = f"""
    **Role**: You are an expert lead architect tasked with managing a conversation between the cloud and open-source architects. You will review each result and choose the best solution.You will striclty use any number of summary tables format to communicate your decision.
    {task}
    """

    # Agents setup
    user = UserProxyAgent(name="Supervisor",
                          system_message="A human head of the Architecture team",
                          code_execution_config={"last_n_messages": 2, "work_dir": "groupchat", "use_docker":False, "human_input_mode": "Never"}
                          )

    cloud_agent = AssistantAgent(name="Cloud Architect",
                                 system_message=cloud_prompt,
                                 llm_config=deepseek_config)

    os_advocate = AssistantAgent(name="Open-source Software Advocate",
                                 system_message=oss_prompt,
                                 llm_config=deepseek_config)

    lead_architect = AssistantAgent(name="Lead Architect of Team",
                                    system_message=lead_prompt,
                                    llm_config=deepseek_config)

    def state_transition(last_speaker, groupchat):
        if last_speaker is user:
            return cloud_agent
        elif last_speaker is cloud_agent:
            return os_advocate
        elif last_speaker is os_advocate:
            return lead_architect
        elif last_speaker is lead_architect:
            return None

    groupchat = GroupChat(
        agents=[user, cloud_agent, os_advocate, lead_architect],
        messages=[],
        max_round=10,
        speaker_selection_method=state_transition
    )

    manager = GroupChatManager(groupchat=groupchat,
                               llm_config=llm_config)

    return user, manager






# Streamlit app UI
st.title('Architecture Proposal Chatbot')
st.write('Provide the task to initiate a conversation among the architects.')

task_input = st.text_area("Enter Business Requirements", height=200)

if st.button('Start Conversation'):
    if task_input:
        user, manager = initialize_agents(task_input)
        
        # Start the chat
        response = user.initiate_chat(
            manager,
            message="Provide your best architecture based on these business requirements"
        )

        # Display chat history
        st.subheader("Conversation History:")
        for entry in response.chat_history:
            # st.markdown(f"{entry['name']}")
            st.markdown(f"**{entry['name']}**: {entry['content']}")
            # st.markdown('''Happy Streamlit-ing! :balloon:''')
            st.divider()

    else:
        st.error("Please enter the business requirements to start.")
        import streamlit as st

