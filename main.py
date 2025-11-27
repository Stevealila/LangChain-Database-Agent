from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from dotenv import load_dotenv
from tools import db_insert_user_tool, db_read_users_tool, db_delete_user_tool

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    system_prompt="You are a helpful assistant",
    tools=[db_insert_user_tool, db_read_users_tool, db_delete_user_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "db_insert_user": {
                    "allowed_decisions": ["approve", "reject"], 
                    "description": "Saving user requires your approval"
                },
            }
        )
    ],
    checkpointer=InMemorySaver()
)


config = {"configurable": {"thread_id":"79"}}


# ...........................................Conversation...............................

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    for update in agent.stream({"messages":[HumanMessage(content=user_input),]}, config, stream_mode="updates"):

        if "__interrupt__" in update:
 
            interrupt = update["__interrupt__"][0]
            action_requests = interrupt.value["action_requests"]
            review_configs = interrupt.value["review_configs"]
            
            for action_req, review_config in zip(action_requests, review_configs):
                
                print(f"INTERRUPT: {action_req.get('description', 'Action requires approval')}")

                new_user_name = action_req['args'].get('name', '')
                new_user_email = action_req['args'].get('email', '')
                
                allowed = review_config.get("allowed_decisions", ["approve", "reject"])
                print(f"Are sure you want to add {new_user_name}, {new_user_email}? Allowed decisions: {', '.join(allowed)}")
                
                decision_type = input("\nYour decision (approve/reject): ").strip().lower()
                
                if decision_type not in allowed:
                    print(f"Invalid decision. Must be one of: {', '.join(allowed)}")
                    decision_type = "reject"
                
                my_interrupt_decision = decision_type

            print(my_interrupt_decision)

            resume_response = agent.invoke(
                Command(
                    resume={"decisions": [{"type": my_interrupt_decision}]}
                ),
                config=config
            )
            print("================================== Ai Message ==================================\n")
            print(resume_response["messages"][-1].content)

        else:
            for node_name, node_update in update.items():
                if node_update and "messages" in node_update:
                    for message in node_update["messages"]:
                        message.pretty_print()