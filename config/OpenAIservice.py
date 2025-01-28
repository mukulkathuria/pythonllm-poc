from openai import OpenAI
import os


class OpenAIService:
    def __init__(self):
        self.openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    async def createThread(self):
        thread = self.openai.beta.threads.create()
        return thread.id

    async def respondToMessage(self ,chathistory):
        try:
            chatCompletion = self.openai.chat.completions.create(
                model= self.model,
                messages=chathistory,
            )
            return {  'data': chatCompletion.choices[0].message.content }
        except self.openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except self.openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except self.openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
  

    async def addFunctionOutput(self ,threadId, runId, output):
        try:
            res = self.openai.beta.threads.runs.submit_tool_outputs(
            thread_id = threadId,
            run_id = runId,
            tool_outputs = output
            )
            return { 'data': res }
        except self.openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except self.openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except self.openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
  

    async def addMessage(self ,threadId, assistantId, message): 
        try: 
            response = self.openai.beta.threads.messages.create(thread_id = threadId, role= 'user', message=message)
            run =  self.openai.beta.threads.runs.create_and_poll(
                    thread_id=threadId,
                    assistant_id=assistantId,
                    )
            return { 'data': run };
        except self.openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except self.openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except self.openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)

