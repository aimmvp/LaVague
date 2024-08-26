from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
from dotenv import load_dotenv

from lavague.core.token_counter import TokenCounter
from lavague.contexts.openai import OpenaiContext
from lavague_config import *


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
inst1 = """
- Enter {} in the 'Email ID' field, {} in the 'Password' field, and click the '로그인' button.
- '데이터 분석 입문자를 위한 통계와 머신러닝 기초' 강의의 강사는 누구지?
""".format(
    TEST_ID, TEST_PWD
)

inst2 = """
- Enter {} in the 'Email ID' field, {} in the 'Password' field, and click the '로그인' button.
- 지금까지 학습한 학습시간은 몇 분이지?
""".format(
    TEST_ID, TEST_PWD
)

inst3 = """
- Enter {} in the 'Email ID' field, {} in the 'Password' field, and click the '로그인' button.
- 화면의 오른쪽에 있는 초록색 원안에 있는 하얀색 화살표를 클릭한다.
- 내가 획득한 Badge 목록은?
""".format(
    TEST_ID, TEST_PWD
)

# Set URL
agent.get(TEST_URL)

ret = agent.run(inst3)
print("결과 : ", ret.output)
