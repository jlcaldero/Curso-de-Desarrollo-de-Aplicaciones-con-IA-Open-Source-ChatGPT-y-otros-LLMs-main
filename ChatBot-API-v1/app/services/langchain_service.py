from langchain.prompts import ChatPromptTemplate
# from langchain.schema import MessagesPlaceholder
from langchain.chains import LLMChain
# from langchain.chat_models import ChatOpenAI  # Suponiendo que estás usando OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from app.services.agents.base_agent import BaseAgent

class LanchainService():

    async def getInstruction(self,  agent: BaseAgent) -> str:

        with open('./app/services/agents/' + agent.layer + '/instruction.txt', 'r', encoding='utf-8') as file:
            instruction = file.read()

        return instruction


    async def chat(self, agent: BaseAgent, inputMessage: str, context: str) -> str:
        # try:
            print('estoy en chat !')
            print('AGENTE ' + agent.layer)
            inputSystem = await self.getInstruction(
                agent,
            )
            print('inputSystem ' + inputSystem)

            prompt = ChatPromptTemplate([
                ("system", '{system}'),
                ("human", '{input}'),
            ])

            complete_system_prompt = inputSystem.replace("{Context}", context)

            model = ChatOpenAI(
                model="gpt-4o",
                temperature=0.5,
            )

            chain = prompt.pipe(model)
            
            response = chain.invoke({
                'system': complete_system_prompt,
                'input': inputMessage
            })

            return response.content
        # except Exception as e:
        #     raise Exception('Internal Server Error') from e
