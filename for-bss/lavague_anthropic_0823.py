from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent
from dotenv import load_dotenv

from lavague.core.token_counter import TokenCounter
from lavague.contexts.anthropic import AnthropicContext

# import TokenCounter
from lavague.core.token_counter import TokenCounter
from lavague.core.logger import LocalLogger

from lavague_config import *

log = LocalLogger(log_file_path="log_anthropic.txt")

# API KEY 정보로드
load_dotenv()

# instantiate it before all other modules
token_counter = TokenCounter(log=True)

# LLM 모델 선택
llm_context = context = AnthropicContext()

# Set up our three key components: Driver, Action Engine, World Model
driver = SeleniumDriver(headless=False)
action_engine = ActionEngine.from_context(context=llm_context, driver=driver)
world_model = WorldModel.from_context(llm_context)
world_model.add_knowledge("lavague_anthropic_knowledge.txt")

# Create Web Agent
agent = WebAgent(world_model, action_engine, token_counter=token_counter, logger=log)

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
ret = agent.run(inst3, log_to_db=True)
print("결과 : ", ret.output)

# get logs
log_df = agent.logger.return_pandas()

# compute and show steps taken, tokens consummed and cost
total_cost = log_df["total_step_cost"].sum()
total_tokens = log_df["total_step_tokens"].sum()
total_steps = len(log_df)

print("Total steps:", total_steps)
print(f"Total tokens: {total_tokens}")
print(f"Total cost: ${round(total_cost, 3)}")


# 결과 :  The user has not acquired any badges yet. The system displays a message saying "획득한 Badge가 없습니다." which translates to "There are no acquired badges."
# Total steps: 7
# Total tokens: 257301
# Total cost: $0.662

# Add knowledge
# 결과 :  The user currently has not acquired any badges. The system encourages the user to earn badges through learning activities, stating "Acquire badges through learning and get your knowledge and skills certified!"
# Total steps: 5
# Total tokens: 101704
# Total cost: $0.276
