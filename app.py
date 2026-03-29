from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from graph import create_graph
from config import CHECKPOINTER_DB_PATH, RECURSION_LIMIT




def main():

    thread_id = input("Enter the thread ID: ").strip()
    print("\n\n\n")

    with SqliteSaver.from_conn_string(CHECKPOINTER_DB_PATH) as checkpointer:

        multiagent = create_graph(checkpointer)

        config = {
            "configurable": {
                "thread_id": thread_id
            },
            "recursion_limit": RECURSION_LIMIT
        }

        while True:

            user_input = input("Enter your message: ").strip()

            if user_input.lower() in ["exit", "quit", "bye"]:
                break

            if not user_input:
                continue

            print(f"---> User message:\n{user_input}\n\n\n")

            snapshot = multiagent.get_state(config=config)

            messages = snapshot.values.get("messages", [])

            messages = messages + [HumanMessage(content=user_input)]

            state = {
                "messages": messages,
                "subagent_messages": [],
                "subagent_result": "",
                "route": ""
            }

            new_state = multiagent.invoke(state, config=config)

            last_message = new_state["messages"][-1]

            print(f"---> Agent message:\n{last_message.content}\n\n\n")



if __name__ == "__main__":

    main()