import asyncio
from langchain_core.messages import HumanMessage
from src.rag.graph_builder import builder

async def test_query():
    messages = [HumanMessage(content="explain what all things are mentioned in the 3rd section of the pdf uploaded here")]
    
    try:
        result = builder.invoke({
            "messages": messages,
            "user_id": "test_user_123"
        })
        print(result["messages"][-1].content)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_query())
