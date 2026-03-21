import time
from langchain_core.messages import HumanMessage
from src.graph import graph

def main():
    print("Welcome to the MODULAR AI Story Generator!")
    user_theme = input("\nWhat kind of story do you want to hear? ")

    # 1. Initialize the first state
    state = {
        "user_input": user_theme,
        "messages": [HumanMessage(content=user_theme)],
        "draft_story": "",
        "research_data": None,
        "judge_feedback": None,
        "status": "retry_writer",
        "needs_search": False,
        "retry_count": 0
    }
    config = {"configurable": {"thread_id": "modular_1"}, "recursion_limit": 20}

    while True:
        start_time = time.time()
        
        # Invoke the graph
        final_state = graph.invoke(state, config=config)
        duration = time.time() - start_time
        
        if final_state.get("status") == "rejected":
            print("\n--- STORY REJECTED ---")
            print(f"Reason: {final_state.get('rejection_reason')}")
            print(f"Time: {duration:.2f}s")
            feedback = input("Try a safer theme (or type 'end'): ")
            if not feedback or feedback.strip().lower() == "end":
                break
            # Reset state for new attempt
            state["user_input"] = feedback
            state["messages"] = [HumanMessage(content=feedback)]
            state["status"] = "retry_writer"
            state["needs_search"] = False
            state["research_data"] = None
            state["retry_count"] = 0
            continue

        print("\n" + "="*50)
        print("\n--- STORY APPROVED ---")
        print(f"Time: {duration:.2f}s")
        print("\n" + final_state.get("draft_story", ""))
        print("\n" + "="*50)
        
        feedback = input("\nAdd a story beat or type 'end': ")
        
        if not feedback or feedback.strip().lower() == "end":
            print("Sweet dreams!")
            break

        # Update state for next turn
        state["user_input"] = feedback
        state["messages"].append(HumanMessage(content=feedback))
        state["status"] = "retry_writer"
        state["needs_search"] = False
        state["research_data"] = None
        state["retry_count"] = 0

if __name__ == "__main__":
    main()
