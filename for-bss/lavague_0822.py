# Install necessary elements
from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
from dotenv import load_dotenv

from lavague.core.token_counter import TokenCounter
from lavague.contexts.openai import OpenaiContext

from lavague_config import *

# from lavague_config import TEST_PWD

# API KEY 정보로드
load_dotenv()

# LLM 모델 선택
llm_model = "gpt-4o"
llm_context = OpenaiContext(llm=llm_model, mm_llm=llm_model)

# Set up our three key components: Driver, Action Engine, World Model
driver = SeleniumDriver(headless=False)
action_engine = ActionEngine.from_context(context=llm_context, driver=driver)
world_model = WorldModel.from_context(llm_context)

# Create Web Agent
agent = WebAgent(world_model, action_engine)

# Instruction
instruction = """
- 로그인을 한다. email ID : {}, 비밀번호: {}
- Certification  페이지로 이동한다.
""".format(
    TEST_ID, TEST_PWD
)

# Set URL
agent.get(TEST_URL)

agent.run(instruction)
